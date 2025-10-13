"""
Tests for Template Tags
"""

# System Imports.
from collections import namedtuple

# Third-Party Imports.
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, AnonymousUser
from django.forms import BaseFormSet
from django.template import Template, Context
from django.test import TestCase, override_settings, RequestFactory

# Internal Imports.
from adminlte2_pdq.templatetags import adminlte_tags


# Module Variables.
UserModel = get_user_model()


class TemplateTagTestCase(TestCase):
    """Tests for template tags and associated helper methods."""

    # region Helper Logic

    class TestForm(forms.Form):
        """Test Form"""

        adminlte2_show_field_errors_in_summary = True

        test_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
        test_checkbox = forms.BooleanField(required=False)
        test_select = forms.ChoiceField(required=False)
        test_date = forms.DateField(required=False)
        test_text = forms.CharField(required=False)

    def assertInHTML(self, needle, haystack, **kwargs):
        """Override assertInHTML to show response if not found"""
        try:
            super().assertInHTML(needle, haystack, **kwargs)
        except AssertionError as err:
            message = err.args[0]
            message += f"\n---\n{haystack}\n---\n"
            err.args = (message,)
            raise err

    def assertNotInHTML(self, needle, haystack, **kwargs):
        """Creates a new method to ensure that HTML does not show up"""
        try:
            super().assertInHTML(needle, haystack, **kwargs)
            message = f"{needle} Unexpectedly found in {haystack}"
            raise AssertionError(message)
        except AssertionError:
            pass

    # endregion Helper Logic

    # region Setup

    def setUp(self):
        self.super_user = None
        self.staff_user = None

    def _setup_staff_user(self, permissions=None):
        """Setup Staffuser"""

        # Remove user if already exists.
        if self.staff_user:
            self.staff_user.delete()

        self.staff_user = UserModel()
        self.staff_user.username = "teststaffuser"
        self.staff_user.is_staff = True
        self.staff_user.save()

        if permissions:
            if isinstance(permissions, str):
                permissions = [permissions]
            for permission in permissions:
                perm_object = Permission.objects.filter(
                    codename__exact=permission,
                ).first()
                self.staff_user.user_permissions.add(perm_object)

    def _setup_super_user(self):
        """Setup Superuser"""

        # Remove user if already exists.
        if self.super_user:
            self.super_user.delete()

        self.super_user = UserModel()
        self.super_user.username = "testsuperuser"
        self.super_user.first_name = "David"
        self.super_user.last_name = "Barnes"
        self.super_user.is_superuser = True
        self.super_user.save()

    # endregion Setup

    # region Template Tag Helper Functions

    def test_function__update_errors_with_formset_data(self):
        """Test function update errors with formset data"""

        with self.subTest("Verify returns errors for formset with one formset error"):

            class TestFormSet(BaseFormSet):
                """Test Formset"""

                def clean(self):
                    raise forms.ValidationError("Test Non Form Error")

            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            data = {
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-MAX_NUM_FORMS": "1",
                "form-0-test_text": "text_value",
            }

            TestFormSets = forms.formset_factory(self.TestForm, formset=TestFormSet)

            formset = TestFormSets(data)
            formset.adminlte2_use_error_summary = True

            # pylint:disable=protected-access
            adminlte_tags._update_errors_with_formset_data(errors, formset)

            self.assertTrue(errors["has_non_form_errors"])

        with self.subTest("Verify returns errors for formset with one form error"):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            data = {
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-MAX_NUM_FORMS": "1",
                "form-0-test_text": "text_value",
            }

            TestFormSets = forms.formset_factory(self.TestForm)

            formset = TestFormSets(data)
            formset.adminlte2_use_error_summary = True

            formset.forms[0].add_error(None, "Test Form Error")

            # pylint:disable=protected-access
            adminlte_tags._update_errors_with_formset_data(errors, formset)

            self.assertTrue(errors["has_non_field_errors"])

        with self.subTest("Verify returns errors for formset with one form field error"):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            data = {
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-MAX_NUM_FORMS": "1",
                "form-0-test_text": "text_value",
            }

            TestFormSets = forms.formset_factory(self.TestForm)

            formset = TestFormSets(data)
            formset.adminlte2_use_error_summary = True
            formset.forms[0].add_error("test_text", "Test Field Error")

            # pylint:disable=protected-access
            adminlte_tags._update_errors_with_formset_data(errors, formset)

            self.assertTrue(errors["has_field_errors"])
            self.assertEqual(len(errors["forms"]), 1)

        with self.subTest("Verify throws attribute error when formset is not valid"):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            formset = namedtuple("Form", ["adminlte2_use_error_summary"])
            formset.adminlte2_use_error_summary = True

            with self.assertRaises(AttributeError):
                # pylint:disable=protected-access
                adminlte_tags._update_errors_with_formset_data(errors, formset)

        with self.subTest("Verify returns unmodified errors dict if form does not have use_error summary set"):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            formset = namedtuple("Form", ["adminlte2_use_error_summary"])
            formset.adminlte2_use_error_summary = False

            # pylint:disable=protected-access
            adminlte_tags._update_errors_with_formset_data(errors, formset)

            self.assertEqual(errors["forms"], [])
            self.assertEqual(errors["has_non_form_errors"], False)
            self.assertEqual(errors["has_non_field_errors"], False)
            self.assertEqual(errors["has_field_errors"], False)

    def test_function___update_errors_with_form_data(self):
        """Test function update errors with form data"""

        with self.subTest("Verify returns errors for form with one form error"):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            data = {"form-0-test_text": "text_value"}

            form = self.TestForm(data)

            form.add_error(None, "Test Form Error")

            # pylint:disable=protected-access
            adminlte_tags._update_errors_with_form_data(errors, form)

            self.assertTrue(errors["has_non_field_errors"])

        with self.subTest("Verify returns errors for form with one form field error"):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            data = {"form-0-test_text": "text_value"}

            form = self.TestForm(data)
            form.add_error("test_text", "Test Field Error")

            # pylint:disable=protected-access
            adminlte_tags._update_errors_with_form_data(errors, form)

            self.assertTrue(errors["has_field_errors"])
            self.assertEqual(len(errors["forms"]), 1)

        with self.subTest("Verify returns errors for form with both a form error and a form field error"):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            data = {"form-0-test_text": "text_value"}

            form = self.TestForm(data)

            form.add_error(None, "Test Form Error")
            form.add_error("test_text", "Test Field Error")

            # pylint:disable=protected-access
            adminlte_tags._update_errors_with_form_data(errors, form)

            self.assertTrue(errors["has_non_field_errors"])
            self.assertTrue(errors["has_field_errors"])
            self.assertEqual(len(errors["forms"]), 1)

        with self.subTest(
            "Verify returns errors for form with a form error, a form field error, and display summary disabled"
        ):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            data = {"form-0-test_text": "text_value"}

            form = self.TestForm(data)
            form.adminlte2_show_field_errors_in_summary = False

            form.add_error(None, "Test Form Error")
            form.add_error("test_text", "Test Field Error")

            # pylint:disable=protected-access
            adminlte_tags._update_errors_with_form_data(errors, form)

            self.assertTrue(errors["has_non_field_errors"])
            self.assertTrue(errors["has_field_errors"])
            self.assertEqual(len(errors["forms"]), 0)

        with self.subTest("Verify throws attribute error when form is not valid"):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            form = namedtuple("Form", ["adminlte2_use_error_summary"])
            form.adminlte2_use_error_summary = True

            with self.assertRaises(AttributeError):
                # pylint:disable=protected-access
                adminlte_tags._update_errors_with_form_data(errors, form)

        with self.subTest("Verify returns an unmodified errors dict, if the form does not have use_error_summary set"):
            errors = {
                "forms": [],
                "has_non_form_errors": False,
                "has_non_field_errors": False,
                "has_field_errors": False,
            }

            form = namedtuple("Form", ["adminlte2_use_error_summary"])
            form.adminlte2_use_error_summary = False

            # pylint:disable=protected-access
            adminlte_tags._update_errors_with_form_data(errors, form)

            self.assertEqual(errors["forms"], [])
            self.assertEqual(errors["has_non_form_errors"], False)
            self.assertEqual(errors["has_non_field_errors"], False)
            self.assertEqual(errors["has_field_errors"], False)

    # endregion Template Tag Helper Functions

    # region render_form_error_summary Function

    def test_templatetag__render_form_error_summary__formsets(self):
        """Test templatetag render form error summary formsets"""

        with self.subTest("Verify summary does not display errors if there are none"):
            TestFormSets = forms.formset_factory(self.TestForm)

            formset = TestFormSets(
                {
                    "form-TOTAL_FORMS": "1",
                    "form-INITIAL_FORMS": "0",
                    "form-MAX_NUM_FORMS": "",
                    "form-0-test_text": "text_value",
                }
            )
            formset.adminlte2_use_error_summary = True

            context = Context(
                {
                    "formset": formset,
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

            rendered_template = template_to_render.render(context)

            self.assertNotIn("Test Field Error", rendered_template)

        with self.subTest("Verify displays field errors for a single formset with one field error"):
            TestFormSets = forms.formset_factory(self.TestForm)

            formset = TestFormSets(
                {
                    "form-TOTAL_FORMS": "1",
                    "form-INITIAL_FORMS": "0",
                    "form-MAX_NUM_FORMS": "",
                    "form-0-test_text": "text_value",
                }
            )
            formset.adminlte2_use_error_summary = True

            formset.forms[0].add_error("test_text", "Test Field Error")

            context = Context(
                {
                    "formset": formset,
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Test Field Error", rendered_template)

        with self.subTest("Verify displays field errors for a list of formsets with one field error"):
            TestFormSets = forms.formset_factory(self.TestForm)

            test_formset = TestFormSets(
                {
                    "form-TOTAL_FORMS": "1",
                    "form-INITIAL_FORMS": "0",
                    "form-MAX_NUM_FORMS": "",
                    "form-0-test_text": "text_value",
                }
            )
            test_formset.adminlte2_use_error_summary = True

            test_formset_2 = TestFormSets(
                {
                    "form-TOTAL_FORMS": "1",
                    "form-INITIAL_FORMS": "0",
                    "form-MAX_NUM_FORMS": "",
                    "form-0-test_text": "text_value",
                }
            )
            test_formset_2.adminlte2_use_error_summary = True

            test_formset.forms[0].add_error("test_text", "Test Field Error")

            context = Context(
                {
                    "test_formset": test_formset,
                    "test_formset_2": test_formset_2,
                    "adminlte2_formset_list": [test_formset, test_formset_2],
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Test Field Error", rendered_template)

        with self.subTest("Verify displays form error for a single formset with one form error"):
            TestFormSets = forms.formset_factory(self.TestForm)

            formset = TestFormSets(
                {
                    "form-TOTAL_FORMS": "1",
                    "form-INITIAL_FORMS": "0",
                    "form-MAX_NUM_FORMS": "",
                    "form-0-test_text": "text_value",
                }
            )
            formset.adminlte2_use_error_summary = True

            formset.forms[0].add_error(None, "Test Form Error")

            context = Context(
                {
                    "formset": formset,
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Test Form Error", rendered_template)

        with self.subTest("Verify displays formset errors for a single formset with one formset error"):

            class TestFormSet(BaseFormSet):
                """Test Formset"""

                def clean(self):
                    raise forms.ValidationError("Test Non Form Error")

            data = {
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-MAX_NUM_FORMS": "1",
                "form-0-test_text": "text_value",
            }

            TestFormSets = forms.formset_factory(self.TestForm, formset=TestFormSet)

            formset = TestFormSets(data)
            formset.adminlte2_use_error_summary = True

            context = Context(
                {
                    "formset": formset,
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Test Non Form Error", rendered_template)

    def test_templatetag__render_form_error_summary__forms(self):
        """Test templatetag render form error summary forms"""

        with self.subTest("Verify does not display errors if there are none"):
            form = self.TestForm({"test_text": "text_value"})

            context = Context(
                {
                    "form": form,
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

            rendered_template = template_to_render.render(context)

            self.assertNotIn("Test Field Error", rendered_template)

        with self.subTest("Verify displays field errors for a single form with one field error"):
            form = self.TestForm({"test_text": "text_value"})

            form.add_error("test_text", "Test Field Error")

            context = Context(
                {
                    "form": form,
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Test Field Error", rendered_template)

        with self.subTest("Verify displays field errors for a list of forms each with one field error"):
            test_form = self.TestForm({"test_text": "text_value"})
            test_form.add_error("test_text", "Test Field Error")

            test_form_2 = self.TestForm({"test_text": "text_value"})
            test_form_2.add_error("test_text", "Test Field Error 2")

            context = Context(
                {"test_form": test_form, "test_form2": test_form_2, "adminlte2_form_list": [test_form, test_form_2]}
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Test Field Error", rendered_template)

        with self.subTest("Verify displays form errors for a single form with one form error"):
            form = self.TestForm({"test_text": "text_value"})

            form.add_error(None, "Test Form Error")

            context = Context(
                {
                    "form": form,
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Test Form Error", rendered_template)

    # endregion render_form_error_summary Function

    def test__render_horizontal_formset(self):
        """Test render horizontal formset"""

        with self.subTest("Verify correctly renders a horizontal formset"):
            TestFormSets = forms.formset_factory(self.TestForm)

            formset = TestFormSets(
                {
                    "form-TOTAL_FORMS": "1",
                    "form-INITIAL_FORMS": "0",
                    "form-MAX_NUM_FORMS": "",
                    "form-0-test_text": "text_value",
                }
            )

            context = Context(
                {
                    "formset": formset,
                }
            )

            template_to_render = Template(
                "{% load adminlte_tags %}{% render_horizontal_formset formset 'Test Formset Section' %}"
            )

            rendered_template = template_to_render.render(context)

            self.assertIn("Test Formset Section", rendered_template)
            self.assertInHTML(
                '<input type="hidden" name="form-TOTAL_FORMS" value="1" id="id_form-TOTAL_FORMS" />',
                rendered_template,
            )
            self.assertInHTML(
                '<input type="text" name="form-0-test_text" value="text_value"'
                ' class="form-control" placeholder="Test text" id="id_form-0-test_text" />',
                rendered_template,
            )

    def test__render_horizontal_form(self):
        """Test render horizontal form"""

        with self.subTest("Verify correctly renders a horizontal form"):
            form = self.TestForm({"test_text": "text_value"})

            context = Context(
                {
                    "form": form,
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_horizontal_form form %}")

            rendered_template = template_to_render.render(context)

            self.assertInHTML(
                '<input type="text" name="test_text" value="text_value"'
                ' class="form-control" placeholder="Test text" id="id_test_text" />',
                rendered_template,
            )

        with self.subTest("Verify renders no fields when form is none"):
            form = None

            context = Context({"form": form})

            template_to_render = Template("{% load adminlte_tags %}{% render_horizontal_form form %}")

            rendered_template = template_to_render.render(context)

            self.assertNotInHTML(
                '<input type="text" name="test_text" value="text_value"'
                ' class="form-control" placeholder="Test text" id="id_test_text" />',
                rendered_template,
            )

    def test__render_form(self):
        """Test render form"""

        with self.subTest("Verify correctly renders a form"):
            form = self.TestForm({"test_text": "text_value"})

            context = Context(
                {
                    "form": form,
                }
            )

            template_to_render = Template("{% load adminlte_tags %}{% render_form form %}")

            rendered_template = template_to_render.render(context)

            self.assertInHTML(
                '<input type="text" name="test_text" value="text_value"'
                ' class="form-control" placeholder="Test text" id="id_test_text" />',
                rendered_template,
            )

        with self.subTest("Verify renders no fields when form is none"):
            form = None

            context = Context({"form": form})

            template_to_render = Template("{% load adminlte_tags %}{% render_form form %}")

            rendered_template = template_to_render.render(context)

            self.assertNotInHTML(
                '<input type="text" name="test_text" value="text_value"'
                ' class="form-control" placeholder="Test text" id="id_test_text" />',
                rendered_template,
            )

    def test__get_login_url__no_entry_in_settings(self):
        """Test get login url no entry in settings"""
        context = Context({})

        template_to_render = Template("{% load adminlte_tags %}{% get_login_url %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("/accounts/login", rendered_template)

    @override_settings(LOGIN_URL="/foobar/login/")
    def test__get_login_url__entry_in_settings(self):
        """Should fallback to default."""
        context = Context({})

        template_to_render = Template("{% load adminlte_tags %}{% get_login_url %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("/foobar/login", rendered_template)

    def test__get_logout_url__no_entry_in_settings(self):
        """Test get logout url no entry in settings"""
        context = Context({})

        template_to_render = Template("{% load adminlte_tags %}{% get_logout_url %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("/accounts/logout", rendered_template)

    @override_settings(LOGOUT_URL="/foobar/logout/")
    def test__get_logout_url__entry_in_settings(self):
        """Should fallback to default."""
        context = Context({})

        template_to_render = Template("{% load adminlte_tags %}{% get_logout_url %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("/foobar/logout", rendered_template)

    def test__get_avatar_url(self):
        """Test get avatar url"""

        with self.subTest("Verify returns actual gravatar url when the user has a gravatar"):
            self._setup_super_user()
            self.super_user.email = "barnesdavidj@gmail.com"

            request = RequestFactory().get("/foo")
            request.user = self.super_user

            context = Context({"user": self.super_user, "request": request})

            template_to_render = Template("{% load adminlte_tags %}{% get_avatar_url user=user %}")

            rendered_template = template_to_render.render(context)

            self.assertIn(
                "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=mp",
                rendered_template,
            )

        with self.subTest("Verify returns the default url when the user is anonymous"):
            user = AnonymousUser()

            request = RequestFactory().get("/foo")
            request.user = user

            context = Context({"user": user, "request": request})

            template_to_render = Template("{% load adminlte_tags %}{% get_avatar_url user=user %}")

            rendered_template = template_to_render.render(context)

            self.assertIn(
                "https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=25&amp;d=mp",
                rendered_template,
            )

        with self.subTest("Verify user image initials returns user div correctly, when passed user"):
            self._setup_super_user()
            self.super_user.email = "barnesdavidj@gmail.com"

            request = RequestFactory().get("/foo")
            request.user = self.super_user

            context = Context({"user": self.super_user, "request": request})

            template_to_render = Template("{% load adminlte_tags %}{% user_image_initials user=user %}")

            rendered_template = template_to_render.render(context)

            self.assertIn(
                "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn("D B", rendered_template)
            self.assertIn('title="David Barnes"', rendered_template)

        with self.subTest("Verify user image initials returns user div correctly, when passed user and overrides"):
            self._setup_super_user()
            self.super_user.email = "barnesdavidj@gmail.com"

            request = RequestFactory().get("/foo")
            request.user = self.super_user

            context = Context({"user": self.super_user, "request": request})

            template_to_render = Template(
                "{% load adminlte_tags %}"
                "{% user_image_initials user=user first_name='John' last_name='Doe' initials='J2D' email='a@b.c' %}"
            )

            rendered_template = template_to_render.render(context)

            self.assertIn(
                "https://www.gravatar.com/avatar/5d60d4e28066df254d5452f92c910092?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn("J2D", rendered_template)
            self.assertIn('title="John Doe"', rendered_template)

        with self.subTest("Verify user image initials returns user div correctly, when passed first and last names"):
            self._setup_super_user()
            self.super_user.email = "barnesdavidj@gmail.com"

            request = RequestFactory().get("/foo")
            request.user = self.super_user

            context = Context({"user": self.super_user, "request": request})

            template_to_render = Template(
                "{% load adminlte_tags %}{% user_image_initials first_name='John' last_name='Doe' %}"
            )

            rendered_template = template_to_render.render(context)

            self.assertNotIn(
                "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn(
                "https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn("J D", rendered_template)
            self.assertIn('title="John Doe"', rendered_template)

        with self.subTest("Verify user image initials returns user div correctly, when passed first name only"):
            self._setup_super_user()
            self.super_user.email = "barnesdavidj@gmail.com"

            request = RequestFactory().get("/foo")
            request.user = self.super_user

            context = Context({"user": self.super_user, "request": request})

            template_to_render = Template("{% load adminlte_tags %}{% user_image_initials first_name='John' %}")

            rendered_template = template_to_render.render(context)

            self.assertNotIn(
                "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn(
                "https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn("J", rendered_template)
            self.assertIn('title="John"', rendered_template)

        with self.subTest("Verify user image initials returns user div correctly, when passed last name only"):
            self._setup_super_user()
            self.super_user.email = "barnesdavidj@gmail.com"

            request = RequestFactory().get("/foo")
            request.user = self.super_user

            context = Context({"user": self.super_user, "request": request})

            template_to_render = Template("{% load adminlte_tags %}{% user_image_initials first_name='John' %}")

            rendered_template = template_to_render.render(context)

            self.assertNotIn(
                "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn(
                "https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn("J", rendered_template)
            self.assertIn('title="John"', rendered_template)
            self._setup_super_user()
            self.super_user.email = "barnesdavidj@gmail.com"

            request = RequestFactory().get("/foo")
            request.user = self.super_user

            context = Context({"user": self.super_user, "request": request})

            template_to_render = Template("{% load adminlte_tags %}{% user_image_initials last_name='Doe' %}")

            rendered_template = template_to_render.render(context)

            self.assertNotIn(
                "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn(
                "https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn("D", rendered_template)
            self.assertIn('title="Doe"', rendered_template)

        with self.subTest("Verify user image initials returns user div correctly, when passed initials only"):
            self._setup_super_user()
            self.super_user.email = "barnesdavidj@gmail.com"

            request = RequestFactory().get("/foo")
            request.user = self.super_user

            context = Context({"user": self.super_user, "request": request})

            template_to_render = Template("{% load adminlte_tags %}{% user_image_initials initials='J2D' %}")

            rendered_template = template_to_render.render(context)

            self.assertNotIn(
                "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn(
                "https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn("J2D", rendered_template)
            self.assertNotIn("title=", rendered_template)

        with self.subTest("Verify user image initials returns user div correctly, when passed no arguments"):
            self._setup_super_user()
            self.super_user.email = "barnesdavidj@gmail.com"

            request = RequestFactory().get("/foo")
            request.user = self.super_user

            context = Context({"user": self.super_user, "request": request})

            template_to_render = Template("{% load adminlte_tags %}{% user_image_initials %}")

            rendered_template = template_to_render.render(context)

            self.assertNotIn(
                "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=blank",
                rendered_template,
            )
            self.assertIn(
                "https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=25&amp;d=mp",
                rendered_template,
            )
            self.assertNotIn("title=", rendered_template)

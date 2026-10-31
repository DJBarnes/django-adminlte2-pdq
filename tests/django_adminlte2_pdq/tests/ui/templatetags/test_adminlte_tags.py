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
GRAVATAR = "https://www.gravatar.com/avatar"
USER_EMAIL_HASH = "174c8d8bad97a893e3d3764912c9868d"  # MD5 of the test superuser's email.
NO_EMAIL_HASH = "d41d8cd98f00b204e9800998ecf8427e"  # MD5 of an empty string.
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

    def test__update_errors_with_formset_data__formset_error(self):
        """Returns errors for formset with one formset error."""

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

    def test__update_errors_with_formset_data__form_error(self):
        """Returns errors for formset with one form error."""
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

    def test__update_errors_with_formset_data__field_error(self):
        """Returns errors for formset with one form field error."""
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

    def test__update_errors_with_formset_data__not_a_formset(self):
        """Throws attribute error when formset is not valid."""
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

    def test__update_errors_with_formset_data__error_summary_off(self):
        """Returns unmodified errors dict if form does not have use_error summary set."""
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

    def test__update_errors_with_form_data__form_error(self):
        """Returns errors for form with one form error."""
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

    def test__update_errors_with_form_data__field_error(self):
        """Returns errors for form with one form field error."""
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

    def test__update_errors_with_form_data__form_and_field_errors(self):
        """Returns errors for form with both a form error and a form field error."""
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

    def test__update_errors_with_form_data__field_errors_not_in_summary(self):
        """Returns errors for form with a form error, a form field error, and display summary disabled."""
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

    def test__update_errors_with_form_data__not_a_form(self):
        """Throws attribute error when form is not valid."""
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

    def test__update_errors_with_form_data__error_summary_off(self):
        """Returns an unmodified errors dict, if the form does not have use_error_summary set."""
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

    def test__render_form_error_summary__formset_without_errors(self):
        """Summary does not display errors if there are none."""
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

    def test__render_form_error_summary__formset_field_error(self):
        """Displays field errors for a single formset with one field error."""
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

    def test__render_form_error_summary__formset_list_field_error(self):
        """Displays field errors for a list of formsets with one field error."""
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

    def test__render_form_error_summary__formset_form_error(self):
        """Displays form error for a single formset with one form error."""
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

    def test__render_form_error_summary__formset_error(self):
        """Displays formset errors for a single formset with one formset error."""

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

    def test__render_form_error_summary__form_without_errors(self):
        """Does not display errors if there are none."""
        form = self.TestForm({"test_text": "text_value"})

        context = Context(
            {
                "form": form,
            }
        )

        template_to_render = Template("{% load adminlte_tags %}{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertNotIn("Test Field Error", rendered_template)

    def test__render_form_error_summary__form_field_error(self):
        """Displays field errors for a single form with one field error."""
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

    def test__render_form_error_summary__form_list_field_errors(self):
        """Displays field errors for a list of forms each with one field error."""
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

    def test__render_form_error_summary__form_error(self):
        """Displays form errors for a single form with one form error."""
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
        """Correctly renders a horizontal form."""
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

    def test__render_horizontal_form__no_form(self):
        """Renders no fields when form is none."""
        form = None

        context = Context({"form": form})

        template_to_render = Template("{% load adminlte_tags %}{% render_horizontal_form form %}")

        rendered_template = template_to_render.render(context)

        self.assertNotIn("<input", rendered_template)

    def test__render_form(self):
        """Correctly renders a form."""
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

    def test__render_form__no_form(self):
        """Renders no fields when form is none."""
        form = None

        context = Context({"form": form})

        template_to_render = Template("{% load adminlte_tags %}{% render_form form %}")

        rendered_template = template_to_render.render(context)

        self.assertNotIn("<input", rendered_template)

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

    @override_settings(ADMINLTE2_LOGOUT_URL="/foobar/logout/")
    def test__get_logout_url__entry_in_settings(self):
        """Uses ADMINLTE2_LOGOUT_URL when it is set."""
        context = Context({})

        template_to_render = Template("{% load adminlte_tags %}{% get_logout_url %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("/foobar/logout", rendered_template)

    def _render_with_user(self, template, user):
        """Render the template with the user in the context, as the request's user."""
        request = RequestFactory().get("/foo")
        request.user = user
        return Template("{% load adminlte_tags %}" + template).render(Context({"user": user, "request": request}))

    def _setup_super_user_with_gravatar(self):
        """Set up the superuser, with an email that has a gravatar."""
        self._setup_super_user()
        self.super_user.email = "barnesdavidj@gmail.com"
        return self.super_user

    def test__get_avatar_url(self):
        """Returns the gravatar url of the user's email."""
        rendered_template = self._render_with_user(
            "{% get_avatar_url user=user %}", self._setup_super_user_with_gravatar()
        )

        self.assertIn(f"{GRAVATAR}/{USER_EMAIL_HASH}?s=25&amp;d=mp", rendered_template)

    def test__get_avatar_url__anonymous_user(self):
        """Returns the default gravatar url for anonymous users."""
        rendered_template = self._render_with_user("{% get_avatar_url user=user %}", AnonymousUser())

        self.assertIn(f"{GRAVATAR}/{NO_EMAIL_HASH}?s=25&amp;d=mp", rendered_template)

    def test__user_image_initials__user(self):
        """Uses the user's name and email."""
        rendered_template = self._render_with_user(
            "{% user_image_initials user=user %}", self._setup_super_user_with_gravatar()
        )

        self.assertIn(f"{GRAVATAR}/{USER_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn("D B", rendered_template)
        self.assertIn('title="David Barnes"', rendered_template)

    def test__user_image_initials__user_and_overrides(self):
        """Names, initials, and email passed to the tag override the user's."""
        rendered_template = self._render_with_user(
            "{% user_image_initials user=user first_name='John' last_name='Doe' initials='J2D' email='a@b.c' %}",
            self._setup_super_user_with_gravatar(),
        )

        self.assertIn(f"{GRAVATAR}/5d60d4e28066df254d5452f92c910092?s=50&amp;d=blank", rendered_template)
        self.assertIn("J2D", rendered_template)
        self.assertIn('title="John Doe"', rendered_template)

    def test__user_image_initials__first_and_last_names(self):
        """Without a user, uses the names passed, and the default gravatar."""
        rendered_template = self._render_with_user(
            "{% user_image_initials first_name='John' last_name='Doe' %}", self._setup_super_user_with_gravatar()
        )

        self.assertNotIn(f"{GRAVATAR}/{USER_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn(f"{GRAVATAR}/{NO_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn("J D", rendered_template)
        self.assertIn('title="John Doe"', rendered_template)

    def test__user_image_initials__first_name_only(self):
        """Uses the first name only."""
        rendered_template = self._render_with_user(
            "{% user_image_initials first_name='John' %}", self._setup_super_user_with_gravatar()
        )

        self.assertNotIn(f"{GRAVATAR}/{USER_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn(f"{GRAVATAR}/{NO_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn("J", rendered_template)
        self.assertIn('title="John"', rendered_template)

    def test__user_image_initials__last_name_only(self):
        """Uses the last name only."""
        rendered_template = self._render_with_user(
            "{% user_image_initials last_name='Doe' %}", self._setup_super_user_with_gravatar()
        )

        self.assertNotIn(f"{GRAVATAR}/{USER_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn(f"{GRAVATAR}/{NO_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn("D", rendered_template)
        self.assertIn('title="Doe"', rendered_template)

    def test__user_image_initials__initials_only(self):
        """Uses the initials, without a title."""
        rendered_template = self._render_with_user(
            "{% user_image_initials initials='J2D' %}", self._setup_super_user_with_gravatar()
        )

        self.assertNotIn(f"{GRAVATAR}/{USER_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn(f"{GRAVATAR}/{NO_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn("J2D", rendered_template)
        self.assertNotIn("title=", rendered_template)

    def test__user_image_initials__no_arguments(self):
        """Without arguments, shows the default gravatar image, without a title."""
        rendered_template = self._render_with_user("{% user_image_initials %}", self._setup_super_user_with_gravatar())

        self.assertNotIn(f"{GRAVATAR}/{USER_EMAIL_HASH}?s=50&amp;d=blank", rendered_template)
        self.assertIn(f"{GRAVATAR}/{NO_EMAIL_HASH}?s=50&amp;d=mp", rendered_template)
        self.assertNotIn("title=", rendered_template)

    def test__user_image_initials__size_and_classes(self):
        """User image initials sets the size and classes."""
        template_to_render = Template(
            "{% load adminlte_tags %}"
            "{% user_image_initials first_name='John' last_name='Doe' size=90 class_name='img-circle' %}"
        )

        rendered_template = template_to_render.render(Context({}))

        self.assertIn('class="user-image-replacement-div img-circle"', rendered_template)
        self.assertIn("width: 90px; height: 90px; font-size: 36px;", rendered_template)
        # The image is requested at twice the displayed size.
        self.assertIn("?s=180&amp;d=blank", rendered_template)
        self.assertIn("J D", rendered_template)
        self.assertIn('aria-label="John Doe"', rendered_template)
        self.assertIn('alt=""', rendered_template)

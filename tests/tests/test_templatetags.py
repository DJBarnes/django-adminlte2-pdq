"""
Tests for Template Tags
"""

from collections import namedtuple
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, AnonymousUser
from django.forms import BaseFormSet
from django.template import Template, Context
from django.test import TestCase, override_settings, RequestFactory

from adminlte2_pdq.templatetags import adminlte_filters, adminlte_tags

UserModel = get_user_model()


class TemplateTagTestCase(TestCase):
    """
    Test Template Tags and Helper Methods used in those template tags
    """

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
            message += "\n---\n{0}\n---\n".format(haystack)
            err.args = (message,)
            raise err

    def assertNotInHTML(self, needle, haystack, **kwargs):
        """Creates a new method to ensure that HTML does not show up"""
        try:
            super().assertInHTML(needle, haystack, **kwargs)
            message = "{0} Unexpectedly found in {1}".format(needle, haystack)
            raise AssertionError(message)
        except AssertionError:
            pass

    # |-------------------------------------------------------------------------
    # | Setup
    # |-------------------------------------------------------------------------

    def setUp(self):
        self.superuser = None
        self.staffuser = None

    def _setup_superuser(self):
        """Setup Superuser"""
        self.superuser = UserModel()
        self.superuser.username = "testsuperuser"
        self.superuser.first_name = "David"
        self.superuser.last_name = "Barnes"
        self.superuser.is_superuser = True
        self.superuser.save()

    def _setup_staffuser(self, permissions=None):
        """Setup Staffuser"""
        self.staffuser = UserModel()
        self.staffuser.username = "teststaffuser"
        self.staffuser.is_staff = True
        self.staffuser.save()

        if permissions:
            if isinstance(permissions, str):
                permissions = [permissions]
            for permission in permissions:
                perm_object = Permission.objects.filter(
                    codename__exact=permission,
                ).first()
                self.staffuser.user_permissions.add(perm_object)

    # |-------------------------------------------------------------------------
    # | Adminlte_Filters.py
    # |-------------------------------------------------------------------------

    # |-------------------------------------------------------------------------
    # | Test fieldtype
    # |-------------------------------------------------------------------------

    def test_fieldtype_returns_the_correct_fieldtype_for_hidden_field(self):
        """Test fieldtype returns the correct fieldtype for hidden field"""
        test_form = self.TestForm()
        result = adminlte_filters.fieldtype(test_form["test_hidden"])

        self.assertEqual("HiddenInput", result)

    def test_fieldtype_returns_the_correct_fieldtype_for_checkbox_field(self):
        """Test fieldtype returns the correct fieldtype for checkbox field"""
        test_form = self.TestForm()
        result = adminlte_filters.fieldtype(test_form["test_checkbox"])

        self.assertEqual("CheckboxInput", result)

    def test_fieldtype_returns_the_correct_fieldtype_for_select_field(self):
        """Test fieldtype returns the correct fieldtype for select field"""
        test_form = self.TestForm()
        result = adminlte_filters.fieldtype(test_form["test_select"])

        self.assertEqual("Select", result)

    def test_fieldtype_returns_the_correct_fieldtype_for_date_field(self):
        """Test fieldtype returns the correct fieldtype for date field"""
        test_form = self.TestForm()
        result = adminlte_filters.fieldtype(test_form["test_date"])

        self.assertEqual("DateInput", result)

    def test_fieldtype_returns_the_correct_fieldtype_for_text_field(self):
        """Test fieldtype returns the correct fieldtype for text field"""
        test_form = self.TestForm()
        result = adminlte_filters.fieldtype(test_form["test_text"])

        self.assertEqual("TextInput", result)

    # |-------------------------------------------------------------------------
    # | Test with_attrs
    # |-------------------------------------------------------------------------

    def test_with_attrs_adds_attributes_to_an_existing_form_field(self):
        """Test with attrs adds attributes to an existring form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_attrs(
            test_form["test_text"], '{"attribute-1":"value-1", "attribute-2":"value-2"}'
        )

        self.assertInHTML(
            '<input type="text" name="test_text" attribute-2="value-2"' ' attribute-1="value-1" id="id_test_text" />',
            str(result),
        )

    # |-------------------------------------------------------------------------
    # | Test with_class
    # |-------------------------------------------------------------------------

    def test_with_class_adds_a_class_to_an_existing_form_field(self):
        """Test with class adds a class to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_class(test_form["test_text"], "my-class-name")

        self.assertIn('class="my-class-name"', str(result))

    def test_with_class_handles_missing_field(self):
        """Test with class handles missing field"""
        result = adminlte_filters.with_class(None, "my-class-name")
        self.assertIsNone(result)

    # |-------------------------------------------------------------------------
    # | Test with_data
    # |-------------------------------------------------------------------------

    def test_with_data_adds_data_attributes_to_an_existing_form_field(self):
        """Test with data adds data attributes to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_data(
            test_form["test_text"], '{"attribute-1":"value-1", "attribute-2":"value-2"}'
        )

        self.assertInHTML(
            '<input type="text" name="test_text" data-attribute-2="value-2"'
            ' data-attribute-1="value-1" id="id_test_text" />',
            str(result),
        )

    # |-------------------------------------------------------------------------
    # | Test with_placeholder
    # |-------------------------------------------------------------------------

    def test_with_placeholder_adds_a_default_placeholder_attribute_to_an_existing_form_field(self):
        """Test with placeholder adds a default placeholder attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_placeholder(test_form["test_text"])

        self.assertIn("Test text", str(result))

    def test_with_placeholder_adds_a_specific_placeholder_attribute_to_an_existing_form_field(self):
        """Test with placeholder adds a specific placeholder attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_placeholder(test_form["test_text"], placeholder="My Placeholder Text")

        self.assertIn("My Placeholder Text", str(result))

    def test_with_placeholder_does_not_override_existing_placeholder_on_an_existing_form_field(self):
        """Test with placeholder does not override existing placeholder on an existing form field"""
        # Add a placeholder to field manually before using tag
        test_form = self.TestForm()
        attrs = test_form["test_text"].field.widget.attrs
        attrs["placeholder"] = "Original Placeholder"
        test_form["test_text"].field.widget.attrs = {**test_form["test_text"].field.widget.attrs, **attrs}

        # Use tag
        result = adminlte_filters.with_placeholder(test_form["test_text"])

        # Verify not overwritten
        self.assertIn("Original Placeholder", str(result))

    # |-------------------------------------------------------------------------
    # | Test with_list
    # |-------------------------------------------------------------------------

    def test_with_list_adds_a_default_list_attribute_to_an_existing_form_field(self):
        """Test with list adds a default list attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_list(test_form["test_text"])

        self.assertIn("test_text_list", str(result))

    def test_with_list_adds_a_specific_list_attribute_to_an_existing_form_field(self):
        """Test with list adds a specific list attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_list(test_form["test_text"], name="my_fancy_list")

        self.assertIn("my_fancy_list", str(result))

    # |-------------------------------------------------------------------------
    # | Test with_pattern
    # |-------------------------------------------------------------------------

    def test_with_pattern_adds_a_default_pattern_attribute_to_an_existing_form_field(self):
        """Test with pattern adds a default pattern attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_pattern(test_form["test_text"])

        self.assertIn(r"\([0-9]{3}\) [0-9]{3}-[0-9]{4}", str(result))

    def test_with_pattern_adds_a_specific_pattern_attribute_to_an_existing_form_field(self):
        """Test with pattern adds a specific pattern attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_pattern(test_form["test_text"], pattern=r"[0-9]{3}-[0-9]{4}")

        self.assertIn('pattern="[0-9]{3}-[0-9]{4}"', str(result))

    # |-------------------------------------------------------------------------
    # | Test with_inputmask
    # |-------------------------------------------------------------------------

    def test_with_inputmask_adds_a_default_inputmask_attribute_to_an_existing_form_field(self):
        """Test with inputmask adds a default inputmask attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_inputmask(test_form["test_text"])

        self.assertIn("(999) 999-9999", str(result))

    def test_with_inputmask_adds_a_specific_inputmask_attribute_to_an_existing_form_field(self):
        """Test with inputmask adds a specific inputmask attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_inputmask(test_form["test_text"], inputmask="999-9999")

        self.assertIn("999-9999", str(result))

    # |-------------------------------------------------------------------------
    # | Test with_min
    # |-------------------------------------------------------------------------

    def test_with_min_adds_a_default_min_attribute_to_an_existing_form_field(self):
        """Test with min adds a default min attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_min(test_form["test_text"])

        self.assertIn('min="0"', str(result))

    def test_with_min_adds_a_specific_min_attribute_to_an_existing_form_field(self):
        """Test with min adds a specific min attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_min(test_form["test_text"], min_val=10)

        self.assertIn('min="10"', str(result))

    # |-------------------------------------------------------------------------
    # | Test with_max
    # |-------------------------------------------------------------------------

    def test_with_max_adds_a_default_max_attribute_to_an_existing_form_field(self):
        """Test with max adds a default max attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_max(test_form["test_text"])

        self.assertIn('max="100"', str(result))

    def test_with_max_adds_a_specific_max_attribute_to_an_existing_form_field(self):
        """Test with max adds a specific max attribute to an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_max(test_form["test_text"], max_val=90)

        self.assertIn('max="90"', str(result))

    # |-------------------------------------------------------------------------
    # | Test with_input_type
    # |-------------------------------------------------------------------------

    def test_with_input_type_changes_the_input_type_of_an_existing_form_field(self):
        """Test with input type changes the input_type of an existing form field"""
        test_form = self.TestForm()
        result = adminlte_filters.with_input_type(test_form["test_text"], new_type="url")

        self.assertIn('type="url"', str(result))

    # |-------------------------------------------------------------------------
    # | Test dir
    # |-------------------------------------------------------------------------

    def test_dir_lists_the_directory_of_an_object(self):
        """Test dir lists the directory of an object"""
        test_form = self.TestForm()
        result = adminlte_filters.directory(test_form["test_text"])

        self.assertIn("'as_hidden', 'as_text'", str(result))

    # |-------------------------------------------------------------------------
    # | Test dictionary
    # |-------------------------------------------------------------------------

    def test_dictionary_lists_the_directory_of_an_object(self):
        """Test dictionary lists the directory of an object"""
        test_form = self.TestForm()
        result = adminlte_filters.dictionary(test_form["test_text"])

        self.assertIn("'field': <django.forms.fields.CharField", str(result))

    # |-------------------------------------------------------------------------
    # | Test unsnake
    # |-------------------------------------------------------------------------

    def test_unsnake_converts_underscore_to_spaces_and_capitalizes_first_letter(self):
        """Test unsnake converts underscore to spaces and capitalizes first letter"""
        result = adminlte_filters.unsnake("this_is_only_a_test")

        self.assertIn("This is only a test", result)

    # |-------------------------------------------------------------------------
    # | Test unslugify
    # |-------------------------------------------------------------------------

    def test_unslugify_converts_underscore_to_spaces_and_capitalizes_first_letter(self):
        """Test unslugify converts underscore to spaces and capitalizes first letter"""
        result = adminlte_filters.unslugify("this-is-only-a-test")

        self.assertIn("This is only a test", result)

    # |-------------------------------------------------------------------------
    # | Adminlte_Tags.py
    # |-------------------------------------------------------------------------
    # |-------------------------------------------------------------------------
    # | Test render_form_error_summary and helper methods
    # |-------------------------------------------------------------------------
    # |-------------------------------------------------------------------------
    # | Test _update_errors_with_formset_data
    # |-------------------------------------------------------------------------

    def test_update_errors_with_formset_data_returns_errors_for_formset_with_one_formset_error(self):
        """Test update errors with formset data returns errors for formset
        with one formset error"""

        class TestFormSet(BaseFormSet):
            """Test Formset"""

            def clean(self):
                raise forms.ValidationError("Test Non Form Error")

        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

        data = {
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "0",
            "form-MAX_NUM_FORMS": "1",
            "form-0-test_text": "text_value",
        }

        TestFormSets = forms.formset_factory(self.TestForm, formset=TestFormSet)

        formset = TestFormSets(data)
        formset.adminlte2_use_error_summary = True

        adminlte_tags._update_errors_with_formset_data(errors, formset)

        self.assertTrue(errors["has_non_form_errors"])

    def test_update_errors_with_formset_data_returns_errors_for_formset_with_one_form_error(self):
        """Test update errors with formset data returns errors for formset
        with one form error"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

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

        adminlte_tags._update_errors_with_formset_data(errors, formset)

        self.assertTrue(errors["has_non_field_errors"])

    def test_update_errors_with_formset_data_returns_errors_for_formset_with_one_form_field_error(self):
        """Test update errors with formset data returns errors for formset with
        one form field error"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

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

        adminlte_tags._update_errors_with_formset_data(errors, formset)

        self.assertTrue(errors["has_field_errors"])
        self.assertEqual(len(errors["forms"]), 1)

    def test_update_errors_with_formset_data_throws_attribute_error_when_formset_is_not_a_valid_formset(self):
        """Test update errors with formset data throws attribute error when
        formset is not a valid formset"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

        formset = namedtuple("Form", ["adminlte2_use_error_summary"])
        formset.adminlte2_use_error_summary = True

        with self.assertRaises(AttributeError):
            adminlte_tags._update_errors_with_formset_data(errors, formset)

    def test_update_errors_with_formset_data_returns_an_unmodified_errors_dict_if_the_form_does_not_have_use_error_summary_set(
        self,
    ):
        """Test update errors with formset data returns an unmodified errors
        dict if the form does not have use error summary set"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

        formset = namedtuple("Form", ["adminlte2_use_error_summary"])
        formset.adminlte2_use_error_summary = False

        adminlte_tags._update_errors_with_formset_data(errors, formset)

        self.assertEqual(errors["forms"], [])
        self.assertEqual(errors["has_non_form_errors"], False)
        self.assertEqual(errors["has_non_field_errors"], False)
        self.assertEqual(errors["has_field_errors"], False)

    # |-------------------------------------------------------------------------
    # | Test _update_errors_with_form_data
    # |-------------------------------------------------------------------------

    def test_update_errors_with_form_data_returns_errors_for_form_with_one_form_error(self):
        """Test update errors with form data returns errors for form with one form error"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

        data = {"form-0-test_text": "text_value"}

        form = self.TestForm(data)

        form.add_error(None, "Test Form Error")

        adminlte_tags._update_errors_with_form_data(errors, form)

        self.assertTrue(errors["has_non_field_errors"])

    def test_update_errors_with_form_data_returns_errors_for_form_with_one_form_field_error(self):
        """Test update errors with form data returns errors for form with one form field error"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

        data = {"form-0-test_text": "text_value"}

        form = self.TestForm(data)
        form.add_error("test_text", "Test Field Error")

        adminlte_tags._update_errors_with_form_data(errors, form)

        self.assertTrue(errors["has_field_errors"])
        self.assertEqual(len(errors["forms"]), 1)

    def test_update_errors_with_form_data_returns_errors_for_form_with_one_form_error_and_one_field_error(self):
        """Test update errors with form data returns errors for form with one
        form error and one field error"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

        data = {"form-0-test_text": "text_value"}

        form = self.TestForm(data)

        form.add_error(None, "Test Form Error")
        form.add_error("test_text", "Test Field Error")

        adminlte_tags._update_errors_with_form_data(errors, form)

        self.assertTrue(errors["has_non_field_errors"])
        self.assertTrue(errors["has_field_errors"])
        self.assertEqual(len(errors["forms"]), 1)

    def test_update_errors_with_form_data_returns_errors_for_form_with_one_form_error_and_one_field_error_and_form_with_display_in_summary_disabled(
        self,
    ):
        """Test update errors with form data returns errors for form with one form
        error and one field error and form with display in summary disabled"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

        data = {"form-0-test_text": "text_value"}

        form = self.TestForm(data)
        form.adminlte2_show_field_errors_in_summary = False

        form.add_error(None, "Test Form Error")
        form.add_error("test_text", "Test Field Error")

        adminlte_tags._update_errors_with_form_data(errors, form)

        self.assertTrue(errors["has_non_field_errors"])
        self.assertTrue(errors["has_field_errors"])
        self.assertEqual(len(errors["forms"]), 0)

    def test_update_errors_with_form_data_throws_attribute_error_when_form_is_not_a_valid_form(self):
        """Test update errors with form data throws attribute error when form
        is not a valid form"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

        form = namedtuple("Form", ["adminlte2_use_error_summary"])
        form.adminlte2_use_error_summary = True

        with self.assertRaises(AttributeError):
            adminlte_tags._update_errors_with_form_data(errors, form)

    def test_update_errors_with_form_data_returns_an_unmodified_errors_dict_if_the_form_does_not_have_use_error_summary_set(
        self,
    ):
        """Test update errors with form data returns an unmodified errors dict
        if the form does not have use error summary set"""
        errors = {"forms": [], "has_non_form_errors": False, "has_non_field_errors": False, "has_field_errors": False}

        form = namedtuple("Form", ["adminlte2_use_error_summary"])
        form.adminlte2_use_error_summary = False

        adminlte_tags._update_errors_with_form_data(errors, form)

        self.assertEqual(errors["forms"], [])
        self.assertEqual(errors["has_non_form_errors"], False)
        self.assertEqual(errors["has_non_field_errors"], False)
        self.assertEqual(errors["has_field_errors"], False)

    # |-------------------------------------------------------------------------
    # | Test render_form_error_summary For Formsets
    # |-------------------------------------------------------------------------

    def test_render_form_error_summary_does_not_display_errors_if_there_are_none_for_formset(self):
        """Test render form error summary does not display errors if there are
        none for formset"""
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

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertNotIn("Test Field Error", rendered_template)

    def test_render_form_error_summary_displays_field_errors_for_a_single_formset_with_one_field_error(self):
        """Test render form error summary displays field errors for a single formset
        with one field error"""
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

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("Test Field Error", rendered_template)

    def test_render_form_error_summary_displays_field_errors_for_a_list_of_formsets_with_one_field_error(self):
        """Test render form error summary displays field errors for a list of
        formsets with one field error"""
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

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("Test Field Error", rendered_template)

    def test_render_form_error_summary_displays_form_error_for_a_single_formset_with_one_form_error(self):
        """Test render form error summary displays form error for a single formset
        with one form error"""
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

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("Test Form Error", rendered_template)

    def test_render_form_error_summary_displays_formset_errors_for_a_single_formset_with_one_formset_error(self):
        """Test render form error summary displays formset errors for a single
        formset with one formset error"""

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

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("Test Non Form Error", rendered_template)

    # |-------------------------------------------------------------------------
    # | Test render_form_error_summary For Forms
    # |-------------------------------------------------------------------------

    def test_render_form_error_summary_does_not_display_errors_if_there_are_none_for_a_form(self):
        """Test render form error summary does not display errors if there are
        non for a form"""
        form = self.TestForm({"test_text": "text_value"})

        context = Context(
            {
                "form": form,
            }
        )

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertNotIn("Test Field Error", rendered_template)

    def test_render_form_error_summary_displays_field_errors_for_a_single_form_with_one_field_error(self):
        """Test render form error summary displays field errors for a single
        form with one field error"""
        form = self.TestForm({"test_text": "text_value"})

        form.add_error("test_text", "Test Field Error")

        context = Context(
            {
                "form": form,
            }
        )

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("Test Field Error", rendered_template)

    def test_render_form_error_summary_displays_field_errors_for_a_list_of_forms_each_with_one_field_error(self):
        """Test render form error summary displays field errors for a list of
        forms each with one field error"""
        test_form = self.TestForm({"test_text": "text_value"})
        test_form.add_error("test_text", "Test Field Error")

        test_form_2 = self.TestForm({"test_text": "text_value"})
        test_form_2.add_error("test_text", "Test Field Error 2")

        context = Context(
            {"test_form": test_form, "test_form2": test_form_2, "adminlte2_form_list": [test_form, test_form_2]}
        )

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("Test Field Error", rendered_template)

    def test_render_form_error_summary_displays_form_errors_for_a_single_form_with_one_form_error(self):
        """Test render form error summary displays form errors for a single form
        with one form error"""
        form = self.TestForm({"test_text": "text_value"})

        form.add_error(None, "Test Form Error")

        context = Context(
            {
                "form": form,
            }
        )

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form_error_summary %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("Test Form Error", rendered_template)

    # |-------------------------------------------------------------------------
    # | Test render_horizontal_form
    # |-------------------------------------------------------------------------

    def test_render_horizontal_form_correctly_renders_a_horizontal_form(self):
        """Test render horizontal form correctly renders a horizontal form"""
        form = self.TestForm({"test_text": "text_value"})

        context = Context(
            {
                "form": form,
            }
        )

        template_to_render = Template("{% load adminlte_tags %}" "{% render_horizontal_form form %}")

        rendered_template = template_to_render.render(context)

        self.assertInHTML(
            '<input type="text" name="test_text" value="text_value"'
            ' class="form-control" placeholder="Test text" id="id_test_text" />',
            rendered_template,
        )

    def test_render_horizontal_form_renders_no_fields_when_form_is_none(self):
        """Test render horizontal form renders no fields when form is none"""
        form = None

        context = Context({"form": form})

        template_to_render = Template("{% load adminlte_tags %}" "{% render_horizontal_form form %}")

        rendered_template = template_to_render.render(context)

        self.assertNotInHTML(
            '<input type="text" name="test_text" value="text_value"'
            ' class="form-control" placeholder="Test text" id="id_test_text" />',
            rendered_template,
        )

    # |-------------------------------------------------------------------------
    # | Test render form
    # |-------------------------------------------------------------------------

    def test_render_form_correctly_renders_a_form(self):
        """Test render form correctly renders a form"""
        form = self.TestForm({"test_text": "text_value"})

        context = Context(
            {
                "form": form,
            }
        )

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form form %}")

        rendered_template = template_to_render.render(context)

        self.assertInHTML(
            '<input type="text" name="test_text" value="text_value"'
            ' class="form-control" placeholder="Test text" id="id_test_text" />',
            rendered_template,
        )

    def test_render_form_renders_no_fields_when_form_is_none(self):
        """Test render form renders no fields when form is none"""
        form = None

        context = Context({"form": form})

        template_to_render = Template("{% load adminlte_tags %}" "{% render_form form %}")

        rendered_template = template_to_render.render(context)

        self.assertNotInHTML(
            '<input type="text" name="test_text" value="text_value"'
            ' class="form-control" placeholder="Test text" id="id_test_text" />',
            rendered_template,
        )

    # |-------------------------------------------------------------------------
    # | Test render_horizontal_formset
    # |-------------------------------------------------------------------------

    def test_render_horizontal_formset_correctly_renders_a_horizontal_formset(self):
        """Test render horizontal formset correctly renders a horizontal formset"""
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
            "{% load adminlte_tags %}" "{% render_horizontal_formset formset 'Test Formset Section' %}"
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

    # |-------------------------------------------------------------------------
    # | Test get_logout_url
    # |-------------------------------------------------------------------------

    def test_get_logout_url_returns_correct_url_when_there_is_an_entry_in_settings(self):
        """Test get logout url returns correct url when there is an entry in settings"""
        context = Context({})

        template_to_render = Template("{% load adminlte_tags %}" "{% get_logout_url %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("/accounts/logout", rendered_template)

    @override_settings(LOGOUT_URL="/foobar/logout")
    def test_get_logout_url_returns_correct_url_when_there_is_not_an_entry_in_the_settings_and_default_is_used(self):
        """Test get logout url returns correct url when there is not an entry in
        the settings and default is used"""
        context = Context({})

        template_to_render = Template("{% load adminlte_tags %}" "{% get_logout_url %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("/foobar/logout", rendered_template)

    # |-------------------------------------------------------------------------
    # | Test get_avatar_url
    # |-------------------------------------------------------------------------

    def test_get_avatar_url_returns_an_actual_gravatar_url_when_the_user_has_a_gravatar(self):
        """Test get avatar url returns an actual gravatar url when the user has a gravatar"""
        self._setup_superuser()
        self.superuser.email = "barnesdavidj@gmail.com"

        request = RequestFactory().get("/foo")
        request.user = self.superuser

        context = Context({"user": self.superuser, "request": request})

        template_to_render = Template("{% load adminlte_tags %}" "{% get_avatar_url user=user %}")

        rendered_template = template_to_render.render(context)

        self.assertIn(
            "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=mp",
            rendered_template,
        )

    def test_get_avatar_url_returns_the_default_url_when_the_user_is_anonymous(self):
        """Test get avatar url returns the default url when the user is anonymous"""
        user = AnonymousUser()

        request = RequestFactory().get("/foo")
        request.user = user

        context = Context({"user": user, "request": request})

        template_to_render = Template("{% load adminlte_tags %}" "{% get_avatar_url user=user %}")

        rendered_template = template_to_render.render(context)

        self.assertIn(
            "https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=25&amp;d=mp",
            rendered_template,
        )

    def test_user_image_initials_returns_user_div_correctly_with_passed_user(self):
        """Test user image initials returns user div correctly with passed user"""
        self._setup_superuser()
        self.superuser.email = "barnesdavidj@gmail.com"

        request = RequestFactory().get("/foo")
        request.user = self.superuser

        context = Context({"user": self.superuser, "request": request})

        template_to_render = Template("{% load adminlte_tags %}" "{% user_image_initials user=user %}")

        rendered_template = template_to_render.render(context)

        self.assertIn(
            "https://www.gravatar.com/avatar/174c8d8bad97a893e3d3764912c9868d?s=25&amp;d=blank",
            rendered_template,
        )
        self.assertIn("D B", rendered_template)
        self.assertIn('title="David Barnes"', rendered_template)

    def test_user_image_initials_returns_user_div_correctly_with_passed_user_and_overrides(self):
        """Test user image initials returns user div correctly with passed user and overrides"""
        self._setup_superuser()
        self.superuser.email = "barnesdavidj@gmail.com"

        request = RequestFactory().get("/foo")
        request.user = self.superuser

        context = Context({"user": self.superuser, "request": request})

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

    def test_user_image_initials_returns_user_div_correctly_with_passed_f_and_l_names(self):
        """Test user image initials returns user div correctly with passed f and l names"""
        self._setup_superuser()
        self.superuser.email = "barnesdavidj@gmail.com"

        request = RequestFactory().get("/foo")
        request.user = self.superuser

        context = Context({"user": self.superuser, "request": request})

        template_to_render = Template(
            "{% load adminlte_tags %}" "{% user_image_initials first_name='John' last_name='Doe' %}"
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

    def test_user_image_initials_returns_user_div_correctly_with_passed_f_name_only(self):
        """Test user image initials returns user div correctly with passed f name only"""
        self._setup_superuser()
        self.superuser.email = "barnesdavidj@gmail.com"

        request = RequestFactory().get("/foo")
        request.user = self.superuser

        context = Context({"user": self.superuser, "request": request})

        template_to_render = Template("{% load adminlte_tags %}" "{% user_image_initials first_name='John' %}")

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

    def test_user_image_initials_returns_user_div_correctly_with_passed_l_name_only(self):
        """Test user image initials returns user div correctly with passed l name only"""
        self._setup_superuser()
        self.superuser.email = "barnesdavidj@gmail.com"

        request = RequestFactory().get("/foo")
        request.user = self.superuser

        context = Context({"user": self.superuser, "request": request})

        template_to_render = Template("{% load adminlte_tags %}" "{% user_image_initials last_name='Doe' %}")

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

    def test_user_image_initials_returns_user_div_correctly_with_passed_initials(self):
        """Test user image initials returns user div correctly with passed initials"""
        self._setup_superuser()
        self.superuser.email = "barnesdavidj@gmail.com"

        request = RequestFactory().get("/foo")
        request.user = self.superuser

        context = Context({"user": self.superuser, "request": request})

        template_to_render = Template("{% load adminlte_tags %}" "{% user_image_initials initials='J2D' %}")

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

    def test_user_image_initials_returns_user_div_correctly_with_no_arguments(self):
        """Test user image initials returns user dive correctly with no arguments"""
        self._setup_superuser()
        self.superuser.email = "barnesdavidj@gmail.com"

        request = RequestFactory().get("/foo")
        request.user = self.superuser

        context = Context({"user": self.superuser, "request": request})

        template_to_render = Template("{% load adminlte_tags %}" "{% user_image_initials %}")

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

"""
Tests for Template Tags
"""

# System Imports.

# Third-Party Imports.
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

# Internal Imports.
from adminlte2_pdq.templatetags import adminlte_filters


# Module Variables.
UserModel = get_user_model()


class TemplateTagTestCase(TestCase):
    """Tests for template tags and associated helper methods."""

    # region Helper Logic

    class TestForm(forms.Form):
        """Example form object for use in tests."""

        adminlte2_show_field_errors_in_summary = True

        test_hidden = forms.CharField(widget=forms.HiddenInput, required=False)
        test_checkbox = forms.BooleanField(required=False)
        test_select = forms.ChoiceField(required=False)
        test_date = forms.DateField(required=False)
        test_text = forms.CharField(required=False)

    def assertInHTML(self, needle, haystack, **kwargs):
        """Override assertInHTML to show response if not found."""
        try:
            super().assertInHTML(needle, haystack, **kwargs)
        except AssertionError as err:
            message = err.args[0]
            message += f"\n---\n{haystack}\n---\n"
            err.args = (message,)
            raise err

    def assertNotInHTML(self, needle, haystack, **kwargs):
        """Creates a new method to ensure that HTML does not show up."""
        try:
            super().assertInHTML(needle, haystack, **kwargs)
            message = f"{needle} Unexpectedly found in {haystack}"
            raise AssertionError(message)
        except AssertionError:
            pass

    # endregion Helper Logic

    # region Setup

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

    # endregion Setup

    def test_filter__fieldtype(self):
        """Tests for the "fieldtype" filter."""

        with self.subTest("Verify returns the correct fieldtype for a hidden field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.fieldtype(test_form["test_hidden"])

            # Verify retrieved value.
            self.assertEqual("HiddenInput", result)

        with self.subTest("Verify returns the correct fieldtype for a checkbox field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.fieldtype(test_form["test_checkbox"])

            # Verify retrieved value.
            self.assertEqual("CheckboxInput", result)

        with self.subTest("Verify returns the correct fieldtype for a select field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.fieldtype(test_form["test_select"])

            # Verify retrieved value.
            self.assertEqual("Select", result)

        with self.subTest("Verify returns the correct fieldtype for a date field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.fieldtype(test_form["test_date"])

            # Verify retrieved value.
            self.assertEqual("DateInput", result)

        with self.subTest("Verify returns the correct fieldtype for a text field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.fieldtype(test_form["test_text"])

            # Verify retrieved value.
            self.assertEqual("TextInput", result)

    def test_filter__with_attrs(self):
        """Tests for the "with_attrs" filter."""

        with self.subTest("Verify adds attributes to existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_attrs(
                test_form["test_text"], '{"attribute-1":"value-1", "attribute-2":"value-2"}'
            )

            # Verify retrieved value.
            self.assertInHTML(
                (
                    '<input type="text" name="test_text" attribute-2="value-2" '
                    'attribute-1="value-1" id="id_test_text" />'
                ),
                str(result),
            )

        # TODO: Should this also have a "handles missing field" like the below test?
        #       In fact, should most of these custom filters?
        #       What is the context that makes "with_class" need to handle a missing field,
        #       yet none of the rest of these do? Doesn't seem documented.

    def test_filter__with_class(self):
        """Tests for the "with_class" filter."""

        with self.subTest("Verify adds class to existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_class(test_form["test_text"], "my-class-name")

            # Verify retrieved value.
            self.assertIn('class="my-class-name"', str(result))

        with self.subTest("Verify handles missing field"):
            result = adminlte_filters.with_class(None, "my-class-name")
            self.assertIsNone(result)

    def test_filter__with_data(self):
        """Tests for the "with_data" filter."""

        with self.subTest("Verify adds data attributes to existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_data(
                test_form["test_text"], '{"attribute-1":"value-1", "attribute-2":"value-2"}'
            )

            # Verify retrieved value.
            self.assertInHTML(
                '<input type="text" name="test_text" data-attribute-2="value-2"'
                ' data-attribute-1="value-1" id="id_test_text" />',
                str(result),
            )

    def test_filter__with_placeholder(self):
        """Tests for the "with_placeholder" filter."""

        with self.subTest("Verify adds a default placeholder attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_placeholder(test_form["test_text"])

            # Verify retrieved value.
            self.assertIn("Test text", str(result))

        with self.subTest("Verify adds a specific placeholder attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_placeholder(test_form["test_text"], placeholder="My Placeholder Text")

            # Verify retrieved value.
            self.assertIn("My Placeholder Text", str(result))

        with self.subTest("Verify does not override existing placeholder on existing form field"):
            # Manually apply some placeholder to form.
            test_form = self.TestForm()
            attrs = test_form["test_text"].field.widget.attrs
            attrs["placeholder"] = "Original Placeholder"
            test_form["test_text"].field.widget.attrs = {**test_form["test_text"].field.widget.attrs, **attrs}

            # Get value from filter.
            result = adminlte_filters.with_placeholder(test_form["test_text"])

            # Verify retrieved value.
            self.assertIn("Original Placeholder", str(result))

    def test_filter__with_list(self):
        """Tests for the "with_list" filter."""

        with self.subTest("Verify adds a default list attribute to existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_list(test_form["test_text"])

            # Verify retrieved value.
            self.assertIn("test_text_list", str(result))

        with self.subTest("Verify adds a default list attribute to existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_list(test_form["test_text"], name="my_fancy_list")

            # Verify retrieved value.
            self.assertIn("my_fancy_list", str(result))

    def test_filter__with_pattern(self):
        """Tests for the "with_pattern" filter."""

        with self.subTest("Verify adds a default pattern attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_pattern(test_form["test_text"])

            # Verify retrieved value.
            self.assertIn(r"\([0-9]{3}\) [0-9]{3}-[0-9]{4}", str(result))

        with self.subTest("Verify adds a specific pattern attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_pattern(test_form["test_text"], pattern=r"[0-9]{3}-[0-9]{4}")

            # Verify retrieved value.
            self.assertIn('pattern="[0-9]{3}-[0-9]{4}"', str(result))

    def test_filter__with_inputmask(self):
        """Tests for the "with_inputmask" filter."""

        with self.subTest("Verify adds a default inputmask attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_inputmask(test_form["test_text"])

            # Verify retrieved value.
            self.assertIn("(999) 999-9999", str(result))

        with self.subTest("Verify adds a specific inputmask attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_inputmask(test_form["test_text"], inputmask="999-9999")

            # Verify retrieved value.
            self.assertIn("999-9999", str(result))

    def test_filter__with_min(self):
        """Tests for the "with_min" filter."""

        with self.subTest("Verify adds a default min attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_min(test_form["test_text"])

            # Verify retrieved value.
            self.assertIn('min="0"', str(result))

        with self.subTest("Verify adds a specific min attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_min(test_form["test_text"], min_val=10)

            # Verify retrieved value.
            self.assertIn('min="10"', str(result))

    def test_filter__with_max(self):
        """Tests for the "with_max" filter."""

        with self.subTest("Verify adds a default max attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_max(test_form["test_text"])

            # Verify retrieved value.
            self.assertIn('max="100"', str(result))

        with self.subTest("Verify adds a specific max attribute to an existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_max(test_form["test_text"], max_val=90)

            # Verify retrieved value.
            self.assertIn('max="90"', str(result))

    def test_filter__with_input_type(self):
        """Tests for the "with_input_type" filter."""

        with self.subTest("Verify changes the input type of existing form field"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.with_input_type(test_form["test_text"], new_type="url")

            # Verify retrieved value.
            self.assertIn('type="url"', str(result))

    def test_filter__dir(self):
        """Tests for the "dir" filter."""

        with self.subTest("Verify lists the directory of an object"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.directory(test_form["test_text"])

            # Verify retrieved value.
            self.assertIn("'as_hidden', 'as_text'", str(result))

    def test_filter__dictionary(self):
        """Tests for the "dictionary" filter."""

        with self.subTest("Verify lists the directory of an object"):
            # Get value from filter.
            test_form = self.TestForm()
            result = adminlte_filters.dictionary(test_form["test_text"])

            # Verify retrieved value.
            self.assertIn("'field': <django.forms.fields.CharField", str(result))

    def test_filter__unsnake(self):
        """Tests for the "unsnake" filter."""

        with self.subTest("Verify converts underscores to spaces and capitalizes first letter"):
            # Get value from filter.
            result = adminlte_filters.unsnake("this_is_only_a_test")

            # Verify retrieved value.
            self.assertIn("This is only a test", result)

    def test_filter__unslugify(self):
        """Tests for the "unslugify" filter."""

        with self.subTest("Verify converts hyphens to spaces and capitalizes first letter"):
            # Get value from filter.
            result = adminlte_filters.unslugify("this-is-only-a-test")

            # Verify retrieved value.
            self.assertIn("This is only a test", result)

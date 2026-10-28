"""
Tests for the skin class template tags and the browser light/dark mode following.
"""

# Third-Party Imports.
from django.test import TestCase, override_settings
from django.urls import reverse

# Internal Imports.
from adminlte2_pdq.templatetags import adminlte_tags


SCRIPT = "adminlte2_pdq/js/extra-features/skin_follow_browser.js"


class SkinClassTagsTestCase(TestCase):
    """Tests for the skin class template tags."""

    def test__light_and_dark_defaults(self):
        """The light and dark skins default from ADMINLTE2_SKIN_CLASS."""
        for skin_class, light, dark in (
            ("skin-blue", "skin-blue", "skin-blue-dark"),
            ("skin-green-light", "skin-green-light", "skin-green-dark"),
            ("skin-red-dark", "skin-red-light", "skin-red-dark"),
            ("skin-black", "skin-black", "skin-black-dark"),
        ):
            with self.subTest(skin_class):
                with override_settings(ADMINLTE2_SKIN_CLASS=skin_class):
                    self.assertEqual(adminlte_tags.get_skin_class_light(), light)
                    self.assertEqual(adminlte_tags.get_skin_class_dark(), dark)

    @override_settings(
        ADMINLTE2_SKIN_CLASS="skin-blue",
        ADMINLTE2_SKIN_CLASS_LIGHT="skin-purple-dark",
        ADMINLTE2_SKIN_CLASS_DARK="skin-green-light",
    )
    def test__light_and_dark_settings_are_used_as_given(self):
        """ADMINLTE2_SKIN_CLASS_LIGHT and ADMINLTE2_SKIN_CLASS_DARK are used without changes."""
        self.assertEqual(adminlte_tags.get_skin_class_light(), "skin-purple-dark")
        self.assertEqual(adminlte_tags.get_skin_class_dark(), "skin-green-light")

    def test__follow_browser_defaults_to_on(self):
        """Following the browser is on unless ADMINLTE2_SKIN_FOLLOW_BROWSER is False."""
        self.assertTrue(adminlte_tags.get_skin_follow_browser())
        with override_settings(ADMINLTE2_SKIN_FOLLOW_BROWSER=False):
            self.assertFalse(adminlte_tags.get_skin_follow_browser())


class SkinFollowBrowserRenderTestCase(TestCase):
    """Tests for the skin attributes and script on rendered pages."""

    @override_settings(ADMINLTE2_SKIN_CLASS="skin-green")
    def test__following_on(self):
        """The body has the light and dark skins, and the script loads right after the body tag."""
        response = self.client.get(reverse("adminlte2_pdq:demo-css"))
        content = response.content.decode()

        self.assertIn('data-skin-current="skin-green"', content)
        self.assertIn('data-skin-light="skin-green"', content)
        self.assertIn('data-skin-dark="skin-green-dark"', content)
        self.assertIn(SCRIPT, content)
        body = content.index("<body")
        self.assertLess(content.index(SCRIPT, body), content.index("sidebar-state.js", body))

    @override_settings(ADMINLTE2_SKIN_CLASS="skin-green", ADMINLTE2_SKIN_FOLLOW_BROWSER=False)
    def test__following_off(self):
        """Only ADMINLTE2_SKIN_CLASS is used: no skin attributes and no script."""
        response = self.client.get(reverse("adminlte2_pdq:demo-css"))
        content = response.content.decode()

        self.assertIn("skin-green", content)
        self.assertNotIn("data-skin-light", content)
        self.assertNotIn(SCRIPT, content)

"""
Takes the screenshots for docs/source/templates/templates.rst, and saves them in docs/img/template/.

Each example in the docs is a template under docs/screenshots/templates/<example>/, which the docs include as is.
For each screenshot, the test project renders a page with that example's folder first in the template folders, in
Firefox (with Selenium).

Run it from the repository root, with the dev packages installed:

    pipenv run pytest docs/screenshots/take_screenshots.py

Environment variables:

    DOCS_SCREENSHOT_EMAIL   The logged-in user's email, for the gravatar. Defaults to the first author's email in
                            pyproject.toml (Python 3.11+). An empty value shows the user's initials.
    FIREFOX_BINARY          The Firefox binary, if Selenium doesn't find a usable one. For the snap Firefox on Ubuntu:
                            /snap/firefox/current/usr/lib/firefox/firefox
    GECKODRIVER             The geckodriver binary, if Selenium doesn't find one. For the snap: /snap/bin/geckodriver

This isn't part of the test suite: the file name doesn't match pytest's test file patterns, so pytest only runs it
when it is named on the command line.
"""

# System Imports.
import datetime
import io
import os
from pathlib import Path

# Third-Party Imports.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service


# Module Variables.
SCREENSHOTS_DIR = Path(__file__).resolve().parent
REPOSITORY_DIR = SCREENSHOTS_DIR.parent.parent
OUTPUT_DIR = REPOSITORY_DIR / "docs" / "img" / "template"
FILE_PREFIX = "django-adminlte2-pdq-"


def screenshot_email():
    """The email of the logged-in user in the screenshots, for the gravatar."""
    if "DOCS_SCREENSHOT_EMAIL" in os.environ:
        return os.environ["DOCS_SCREENSHOT_EMAIL"]
    try:
        import tomllib  # pylint: disable=import-outside-toplevel
    except ImportError:  # Python < 3.11.
        return ""
    with open(REPOSITORY_DIR / "pyproject.toml", "rb") as file:
        return tomllib.load(file)["project"]["authors"][0]["email"]


def templates_with(example):
    """The TEMPLATES setting, with the example's folder searched first. None for the package's own templates."""
    folders = [str(SCREENSHOTS_DIR / "templates" / example)] if example else []
    return [{**settings.TEMPLATES[0], "DIRS": folders}]


@override_settings(ROOT_URLCONF="docs.screenshots.urls", STATICFILES_DIRS=[str(SCREENSHOTS_DIR / "static")])
class TemplateScreenshots(StaticLiveServerTestCase):
    """Screenshots for the templates docs, each before and after an example's change."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        if os.environ.get("FIREFOX_BINARY"):
            options.binary_location = os.environ["FIREFOX_BINARY"]
        service = Service(os.environ["GECKODRIVER"]) if os.environ.get("GECKODRIVER") else Service()
        cls.driver = webdriver.Firefox(options=options, service=service)
        # The gravatar loads from gravatar.com. If it is slow, fail instead of waiting minutes.
        cls.driver.set_page_load_timeout(30)
        cls.driver.set_script_timeout(30)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "david", email=screenshot_email(), password="password", first_name="David", last_name="Barnes"
        )
        # The user dropdown shows when the user joined. A fixed date keeps the screenshots the same on every run.
        self.user.date_joined = datetime.datetime(2026, 1, 15, 9, 30, tzinfo=datetime.timezone.utc)
        self.user.save()

    def log_in(self):
        """Log the browser in as the user."""
        self.client.force_login(self.user)
        # A cookie can only be set on a page of its site.
        self.driver.get(self.live_server_url + "/static/adminlte2_pdq/css/conflicts/conflicts.css")
        self.driver.delete_all_cookies()
        self.driver.add_cookie({"name": "sessionid", "value": self.client.cookies["sessionid"].value, "path": "/"})

    def open(self, example, path, width, height):
        """Open the page with the example's templates, in a window of the given size, and wait for its images."""
        with override_settings(TEMPLATES=templates_with(example)):
            self.driver.set_window_size(width, height)
            self.driver.get(self.live_server_url + path)
            self.driver.execute_script("return document.fonts.ready")
            # Keep the screenshots the same on every run: turn off CSS transitions, so none is caught halfway, and
            # unfocus the field that has autofocus, so neither its focus color nor its blinking cursor shows.
            self.driver.execute_script(
                "const style = document.createElement('style');"
                "style.textContent = '*, *::before, *::after { transition: none !important; }';"
                "document.head.appendChild(style);"
                "document.activeElement.blur();"
            )
            self.driver.execute_script(
                "return Promise.all([...document.images].map("
                "image => image.complete || new Promise(done => { image.onload = image.onerror = done; })))"
            )

    def save(self, png, name):
        """Save a screenshot."""
        Image.open(io.BytesIO(png)).save(OUTPUT_DIR / f"{FILE_PREFIX}{name}.png", optimize=True)

    def test__login_page(self):
        """The login page examples."""
        for example, name in (
            (None, "login-template-original"),
            ("login_no_social", "login-template-no-social"),
            ("login_github", "login-template-github"),
            ("login_more", "login-template-more"),
        ):
            with self.subTest(example=name):
                self.open(example, "/accounts/login/", 800, 620)
                self.save(self.driver.get_screenshot_as_png(), name)

    def test__page(self):
        """The page, and page stylesheets and scripts, examples."""
        self.log_in()
        for example, name in (
            ("page_before", "page-original"),
            ("page", "page-custom"),
            ("page_assets", "page-assets"),
        ):
            with self.subTest(example=name):
                self.open(example, "/reports/monthly/", 1100, 560)
                self.save(self.driver.get_screenshot_as_png(), name)

    def test__footer(self):
        """The footer example."""
        self.log_in()
        for example, name in ((None, "footer-original"), ("footer", "footer-custom")):
            with self.subTest(example=name):
                self.open(example, "/home/", 1100, 700)
                self.save(self.driver.find_element(By.CLASS_NAME, "main-footer").screenshot_as_png, name)

    def test__user_dropdown(self):
        """The user dropdown example."""
        self.log_in()
        for example, name in ((None, "user-dropdown-original"), ("dropdown", "user-dropdown-custom")):
            with self.subTest(example=name):
                self.open(example, "/home/", 1100, 600)
                self.driver.find_element(By.CSS_SELECTOR, ".user-menu > a").click()
                self.driver.execute_script("return new Promise(done => setTimeout(done, 400))")
                menu = self.driver.find_element(By.CSS_SELECTOR, ".user-menu .dropdown-menu")
                self.save(menu.screenshot_as_png, name)

    def test__sidebar(self):
        """The sidebar user panel example: the top of the sidebar, with the logo above it."""
        self.log_in()
        for example, name in ((None, "sidebar-original"), ("sidebar", "sidebar-custom")):
            with self.subTest(example=name):
                self.open(example, "/home/", 1100, 600)
                width = self.driver.find_element(By.CLASS_NAME, "main-sidebar").size["width"]
                page = Image.open(io.BytesIO(self.driver.get_screenshot_as_png()))
                buffer = io.BytesIO()
                page.crop((0, 0, width, 360)).save(buffer, format="PNG")
                self.save(buffer.getvalue(), name)

"""
Project testing settings, so that tests can run project as if it was a proper Django application.
"""

# System Imports.
from warnings import filterwarnings

# Third-party Imports
import django


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}


INSTALLED_APPS = (
    "adminlte2_pdq",
    "tests",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "adminlte2_pdq.middleware.AuthMiddleware",
]


ROOT_URLCONF = "tests.django_adminlte2_pdq.django_test_project.urls"


USE_TZ = True


TIME_ZONE = "UTC"


SECRET_KEY = "test_secret_key"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]


STATIC_URL = "/static/"
MEDIA_URL = "/media/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Make messaging work in tests that use RequestFactory.
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"


# **********************************************
# Added settings to make adminlte2_pdq work
# **********************************************

# Default Profile route does not exist. Change to Home.
LOGIN_REDIRECT_URL = "adminlte2_pdq:home"

ADMINLTE2_ADMIN_INDEX_USE_APP_LIST = True
ADMINLTE2_INCLUDE_ADMIN_HOME_LINK = True
ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES = True
ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES = True

ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST = [
    "/.well-known/appspecific/com.chrome.devtools.json",
]

# ADMINLTE2_MENU_FIRST = []
# ADMINLTE2_MENU = []
# Admin Menu Rendered Between MENU and MENU_LAST
# ADMINLTE2_MENU_LAST = []

# WhiteList
# ADMINLTE2_USE_STRICT_POLICY = (True/False)
# ADMINLTE2_STRICT_POLICY_WHITELIST = []


# region Django Version Specific Settings

# Check to see if on version greater than 5 and fix / suppress warnings from changes in that version.
if django.VERSION >= (5, 0):
    filterwarnings("ignore", "The FORMS_URLFIELD_ASSUME_HTTPS transitional setting is deprecated.")
    FORMS_URLFIELD_ASSUME_HTTPS = True

# endregion Django Version Specific Settings

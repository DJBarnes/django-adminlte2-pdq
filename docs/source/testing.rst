Testing Your Project
********************


Faster Password Hashing
=======================

Django hashes passwords with an algorithm that is slow on purpose, and every
test that creates a user or logs one in pays for it. In the settings that your
tests use, switch to a fast hasher:

.. code:: python

    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]

Use this in test settings only. MD5 is not safe for real passwords.
See Django's
`Speeding up the tests <https://docs.djangoproject.com/en/dev/topics/testing/overview/#speeding-up-the-tests>`_.


Changing Package Settings in Tests
==================================

The package reads its ``ADMINLTE2_*`` settings once, when it is imported, so
``override_settings`` has no effect on them. To change one in a test, patch
the name in the module that uses it. For example, to test a view under the
strict policy:

.. code:: python

    from unittest.mock import patch

    @patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    def test_strict_policy(self):
        ...

The sidebar reads the policy settings in
``adminlte2_pdq.templatetags.sidebar_menu``, so a test that checks sidebar
links patches the names there as well.

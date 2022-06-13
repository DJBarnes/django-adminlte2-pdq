Templates
*********

General
=======

This package comes with a lot of templates that are used right out of the box.
Any and all of these templates can be overridden to customize the look and feel
of the site. Rather than listing out every single file and every single block
within those files that can be overridden, it is preferable that you just
reference the files yourself to see what can be overridden. The files can be
found on
`GitHub <https://github.com/DJBarnes/django-adminlte-2/tree/master/django_adminlte_2/templates>`_.

.. important::

    In ``settings.py``, if you are using
    `APP_DIRS <https://docs.djangoproject.com/en/dev/howto/overriding-templates/#overriding-from-an-app-s-template-directory>`_
    to override templates, you must ensure that the app you are using to house
    those templates is listed in the
    `INSTALLED_APPS <https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-INSTALLED_APPS>`_
    setting before the django-adminlte-2 app. Additionally, the
    django-adminlte-2 app should be listed before any django apps.

For a sample change, see the below instructions.


Example Change
==============

Use the following steps as an example of a change that can be made to change
parts of the site. Let's say that we want to remove or change the login with
social links section from the login page.

.. image:: ../img/template/django-adminlte-2-login-template-original.png
    :alt: Original default login page that comes with django-adminlte-2

We can accomplish this with the following steps:

1.  Create ``registration/login.html`` in one of your django project's
    `template <https://docs.djangoproject.com/en/dev/ref/settings/#templates>`_
    folders defined in your settings file.
2.  Extend the packages default ``registration/login.html`` by adding the
    following line to the file created above.

    .. code:: html+django

        {% extends "registration/login.html" %}

3.  Override the ``social_auth_links`` block. An empty block will remove the
    original content. Additionally, a block with content will replace the
    original content.

    **Removal**

    .. code:: html+django

        {% block social_auth_links %}{% endblock social_auth_links %}

    .. image:: ../img/template/django-adminlte-2-login-template-no-social.png
        :alt: Updated login page with no social links

    **Replacement**

    .. code:: html+django

        {% block social_auth_links %}
          <div class="social-auth-links text-center">
            <p>- OR -</p>
            <a href="#" class="btn btn-block btn-social btn-github btn-flat">
              <i class="fa fa-github"></i>
              Sign in using Github
            </a>
          </div>
        {% endblock social_auth_links %}

    .. image:: ../img/template/django-adminlte-2-login-template-github.png
        :alt: Updated login page with GitHub as the social link.

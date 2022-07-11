.. Django-AdminLTE-2 documentation master file, created by
   sphinx-quickstart on Sat Mar  6 10:30:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django-AdminLTE-2's documentation!
*********************************************

**Django-AdminLTE-2** is a `Django <https://www.djangoproject.com/>`_ app
that takes all of the work out of making a beautiful and functional web
application using the
`AdminLTE2 <https://adminlte.io/themes/AdminLTE/index2.html>`_
theme.

Additionally, the app provides decorators, mixins, template filters, and
template tags to aid in the rapid development of a site.

Features include:

* Styled with `AdminLTE2 <https://adminlte.io/themes/AdminLTE/index2.html>`_.
* Easy sidebar menu creation.
* Automatic
  `Django Admin <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_
  styling that matches AdminLTE2.
* Automatic inclusion of Admin links in the sidebar.
* Automatic menu link hiding based on user permissions to views.
* Template filters to aid in manual styling.
* Template tags for form rendering that matches AdminLTE2.
* Automatic form error and message styling.
* `Font Awesome 4 <https://fontawesome.com/v4/icons/>`_
  & `Font Awesome 5 <https://fontawesome.com/v5/search>`_ integration.
* Highly configurable functionality, via project
  `Django settings variables <https://docs.djangoproject.com/en/dev/topics/settings/>`_.

.. image:: ../img/menu/django-adminlte-2-static-menu.png
    :alt: Site with static menu using settings


.. toctree::
   :maxdepth: 3
   :caption: Getting Started

   quickstart


.. toctree::
   :maxdepth: 3
   :caption: Templates

   templates/templates
   templates/template_filters
   templates/template_tags
   templates/forms
   templates/fields


.. toctree::
   :maxdepth: 3
   :caption: Menu

   menu/general_information
   menu/building_blocks
   menu/advanced
   menu/admin
   menu/examples


.. toctree::
   :maxdepth: 3
   :caption: Configuration

   configuration/home
   configuration/menu
   configuration/admin
   configuration/authorization


.. toctree::
   :maxdepth: 3
   :caption: Authentication & Authorization

   authorization/policies
   authorization/function_views
   authorization/class_views


.. toctree::
   :maxdepth: 3
   :caption: Misc

   demo_css
   api_reference


Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Forms
*****

Forms and formsets can be easily rendered out and properly styled, using the
provided template tags described in the :doc:`template_tags` page.

By default, this package renders form/formset errors the same as Django's
default behavior. IE: forms and formsets will display an error summary with
non-field errors at the top of the form and field errors at each field.

There are a few attributes that you can add to a form to change this behavior
if needed. Those options are explained below.


----


adminlte2_show_field_errors_in_summary
======================================

If you would like to include all field errors in the error summary so that all
errors no matter what type they are show up in the error summary, set this
form attribute to ``True``.

:Type: ``bool``
:Default: ``False``

Example declaring directly on a form class.

.. code:: python

    class MyAwesomeForm(forms.Form):

        adminlte2_show_field_errors_in_summary = True

Example setting on an already instantiated form.

.. code:: python

    form = context['form']
    form.adminlte2_show_field_errors_in_summary = True


adminlte2_use_error_summary
===========================

If you would not like AdminLTE to automatically render out the error summary,
you can turn this off by setting this attribute on your form to ``False``.

This is useful if you want to handle the error summary manually without using
any of the built in magic.

:Type: ``bool``
:Default: ``True``

Example declaring directly on a form class.

.. code:: python

    class MyAwesomeForm(forms.Form):

        adminlte2_use_error_summary = False

Example setting on an already instantiated form.

.. code:: python

    form = context['form']
    form.adminlte2_use_error_summary = False

.. warning::

    By disabling this, there will be no error summary box at all.
    This means that the error summary message and all non-field errors will not
    be shown and must be rendered manually by you.

.. warning::

    Disabling this will override the
    :ref:`templates/forms:adminlte2_show_field_errors_in_summary`
    option and hide all lines in the
    error summary including field errors.

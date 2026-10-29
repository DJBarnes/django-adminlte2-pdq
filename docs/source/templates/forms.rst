Forms
*****

Forms and formsets can be easily rendered out and properly styled, using the
provided template tags described in the :doc:`template_tags` page.

By default, this package renders form/formset errors the same as Django's
default behavior. That is, forms and formsets will display an error summary
with non-field errors at the top of the form and field errors at each field.

There are a few attributes that you can add to a form to change this behavior
if needed. Those options are explained below.


----


Which Forms Are Checked
=======================

Every page that extends ``adminlte2/base.html`` renders the error summary
above the page content, in the ``form_errors`` block, with the
:ref:`templates/template_tags:render_form_error_summary` template tag. The
tag looks for forms and formsets in the template context under these names:

* ``form``: a single form. This is the name Django's generic class-based
  views use.
* ``formset``: a single formset.
* ``adminlte2_form_list``: a list of forms. When it is in the context,
  ``form`` is not checked on its own, so include it in the list if it should
  be checked too.
* ``adminlte2_formset_list``: a list of formsets. When it is in the context,
  ``formset`` is not checked on its own.

Forms under any other name are not checked. To include them, or to check
several forms on one page, put them in ``adminlte2_form_list``:

.. code:: python

    def profile(request):
        user_form = UserForm(request.POST or None, instance=request.user)
        address_form = AddressForm(request.POST or None, instance=request.user.address)
        ...
        return render(request, 'profile.html', {
            'user_form': user_form,
            'address_form': address_form,
            'adminlte2_form_list': [user_form, address_form],
        })

In a class-based view, add the list in ``get_context_data``:

.. code:: python

    class ProfileView(FormView):
        ...

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['adminlte2_form_list'] = [context['form'], self.get_address_form()]
            return context

To leave a form out of the summary, set its
:ref:`templates/forms:adminlte2_use_error_summary` attribute to ``False``.


----


adminlte2_show_field_errors_in_summary
======================================

If you would like to include all field errors in the error summary so that all
errors, no matter what type they are, show up in the error summary, set this
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

If you would not like Django-AdminLTE2-PDQ to automatically render out the error
summary, you can turn this off by setting this attribute on your form to
``False``.

This is useful if you want to handle the error summary manually without using
any of the built-in magic.

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

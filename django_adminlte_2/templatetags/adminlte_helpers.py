"""
Django AdminLTE2 Template Tags

Collection of template tags to make rendering things easier.
"""
from hashlib import md5
import logging

from django import template
from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)
register = template.Library()

# |-----------------------------------------------------------------------------
# | Helper methods for the template tags below
# |-----------------------------------------------------------------------------


def _update_errors_with_formset_data(errors, formset):
    """
    Inspect a formset, determine what types of errors it has, and then return a
    dictionary with the formsets that contain errors and what types of errors.
    """
    try:
        # If the formset has opted in for using the error summary
        if hasattr(formset, 'adminlte2_use_error_summary') and formset.adminlte2_use_error_summary:
            total_error_count = formset.total_error_count()
            if total_error_count > 0:
                non_form_error_count = len(formset.non_form_errors())
                if non_form_error_count > 0:
                    errors['has_non_form_errors'] = True

                form_error_count = total_error_count - non_form_error_count
                # If the formset has any errors at all
                if form_error_count > 0:
                    # Go through each form and collect the errors
                    for form in formset.forms:
                        _update_errors_with_form_data(errors, form)
        return errors
    # Trying to access a property that does not exist. Give some helpful text in error.
    except AttributeError as attribute_error:
        error_message = (
            "The object that you are trying to use for rendering out the formset"
            " and it's subsequent formset errors does not contain required attributes."
            " Original Error: {0}"
        ).format(attribute_error)
        raise AttributeError(error_message) from attribute_error


def _update_errors_with_form_data(errors, form):
    """
    Inspect a form, determine what types of errors it has, and then return a
    dictionary with the forms that contain errors and what types of errors.
    """
    try:
        # If the form has opted in for using the error summary
        if hasattr(form, 'adminlte2_use_error_summary') and form.adminlte2_use_error_summary:
            # If the form has errors
            if form.errors:
                # If there are more field errors than non field errors, which will
                # always be true unless the only errors are non field errors.
                if len(form.errors) > len(form.non_field_errors()):
                    errors['has_field_errors'] = True
                    # The form could have field and non_field errors. Flip the non_field bool
                    if form.non_field_errors():
                        errors['has_non_field_errors'] = True

                    if (
                            hasattr(
                                form,
                                'adminlte2_show_field_errors_in_summary'
                            )
                            and form.adminlte2_show_field_errors_in_summary
                    ):
                        errors['forms'].append(form)
                else:
                    # The only errors are non_field_errors, so flip the bool
                    errors['has_non_field_errors'] = True

        return errors
    # Trying to access property that does not exist. Give some helpful text in error.
    except AttributeError as attribute_error:
        error_message = (
            "The object that you are trying to use for rendering out the forms"
            " and it's subsequent form errors does not contain required attributes."
            " Original Error: {0}"
        ).format(attribute_error)
        raise AttributeError(error_message) from attribute_error


# |-----------------------------------------------------------------------------
# | Render Inclusion Template Tags
# |-----------------------------------------------------------------------------

@register.inclusion_tag('adminlte2/partials/_form_error_summary.html', takes_context=True)
def render_form_error_summary(context):
    """
    Determine if the context contains forms or formsets that should be
    checked for errors, and then add any found errors to the context so they
    can be rendered out at the top of the page.
    """

    # Initialize the errors dictionary
    errors = {
        'forms': [],
        'has_non_form_errors': False,
        'has_non_field_errors': False,
        'has_field_errors': False
    }

    if 'adminlte2_formset_list' in context:
        for formset in context['adminlte2_formset_list']:
            _update_errors_with_formset_data(errors, formset)
    elif 'formset' in context:
        _update_errors_with_formset_data(errors, context['formset'])
        context['adminlte2_formset_list'] = [context['formset']]
    else:
        context['adminlte2_formset_list'] = []

    if 'adminlte2_form_list' in context:
        for form in context['adminlte2_form_list']:
            _update_errors_with_form_data(errors, form)
    elif 'form' in context:
        _update_errors_with_form_data(errors, context['form'])
        context['adminlte2_form_list'] = [context['form']]
    else:
        context['adminlte2_form_list'] = []

    return {
        'error_list': errors,
        'adminlte2_formset_list': context['adminlte2_formset_list'],
        'adminlte2_form_list': context['adminlte2_form_list'],
    }


@register.inclusion_tag('adminlte2/partials/_form.html')
def render_fields(*fields_to_render, **kwargs):
    """Render given fields with optional labels."""
    labels = kwargs.get('labels', True)
    media = kwargs.get('media')
    hidden_fields = []
    visible_fields = []
    for bound_field in fields_to_render:
        if bound_field.field.widget.is_hidden:
            hidden_fields.append(bound_field)
        else:
            visible_fields.append(bound_field)
    return {
        'fields_to_render': fields_to_render,
        'hidden_fields': hidden_fields,
        'visible_fields': visible_fields,
        'labels': labels,
        'media': media,
    }


@register.inclusion_tag('adminlte2/partials/_form.html')
def render_form(form, **kwargs):
    """Render a vertical form."""
    # Send all fields to render_fields which does real logic
    kwargs['media'] = None
    if form:
        kwargs['media'] = form.media
    form = form or []
    fields_to_render = [field for field in form]
    return render_fields(*fields_to_render, **kwargs)


@register.inclusion_tag('adminlte2/partials/_horizontal_form.html')
def render_horizontal_fields(*fields_to_render, **kwargs):
    """Render given fields with optional labels horizontally."""
    labels = kwargs.get('labels', True)
    media = kwargs.get('media')
    hidden_fields = []
    visible_fields = []
    for bound_field in fields_to_render:
        if bound_field.field.widget.is_hidden:
            hidden_fields.append(bound_field)
        else:
            visible_fields.append(bound_field)
    return {
        'fields_to_render': fields_to_render,
        'hidden_fields': hidden_fields,
        'visible_fields': visible_fields,
        'labels': labels,
        'media': media,
    }


@register.inclusion_tag('adminlte2/partials/_horizontal_form.html')
def render_horizontal_form(form, **kwargs):
    """Render a horizontal form."""
    kwargs['media'] = None
    if form:
        kwargs['media'] = form.media
    form = form or []
    fields_to_render = [field for field in form]
    return render_horizontal_fields(*fields_to_render, **kwargs)


@register.inclusion_tag('adminlte2/partials/_horizontal_formset.html')
def render_horizontal_formset(formset, section_heading):
    """Render a horizontal formset."""
    return {
        'formset': formset,
        'section_heading': section_heading,
    }

# |-----------------------------------------------------------------------------
# | Value Simple Template Tags
# |-----------------------------------------------------------------------------


@register.simple_tag()
def get_logout_url():
    """Get the log out URL"""
    return getattr(settings, 'LOGOUT_URL', '/accounts/logout')


@register.simple_tag()
def get_home_url():
    """Get the home URL"""
    return reverse(getattr(settings, 'ADMINLTE2_HOME_ROUTE', 'django_adminlte_2:home'))


@register.simple_tag(takes_context=True)
def get_avatar_url(context, user=None, email=None, size=None, default='mp'):
    """Get a gravatar image url.
    If no image is found, gravatar will return an image based on the 'default'
    keyword. See http://en.gravatar.com/site/implement/images/ for more info.

    This function will get the profile email in this order:
        The 'email' argument,
        The 'user' argument if it has an 'email' attribute,

    NOTE: Method does not work if context is not taken in despite it not using it.
    """
    if not size:
        size = 25

    email = email or ''

    if not email and user and hasattr(user, 'email'):
        email = user.email or ''
    return 'https://www.gravatar.com/avatar/{hash}?s={size}&d={default}'.format(
        hash=md5(
            email.encode('utf-8')
        ).hexdigest(),
        size=size or '',
        default=default,
    )


@register.inclusion_tag('adminlte2/partials/_user_image_initials.html', takes_context=True)
def user_image_initials(
        context,
        user=None,
        email=None,
        initials=None,
        first_name=None,
        last_name=None,
        size=None
):
    """Show user gravatar, initials, or gravatar default mystery person as image

    Attempt to use/create initials of the user in the style of a profile picture.
    Overlay with the user's gravatar image or a blank one if the user does not
    exist. If initials can not be created, change the gravatar default from blank
    to the standard mystery person.

    If the user is passed in, the user will be used for the base information.
    Information can be overridden by other key word arguments.
    If the user is NOT passed in, key word arguments for each piece of information
    should be used.

    Keyword arguments:
    user - the user to use for information
    email - the email to use in place of the users
    initials - the initials to use in place of generated ones from user
    first_name - the first name to use in place of the users
    last_name the last name to use in place of the users
    size - the size of the image. Default is 25X25px

    NOTE: Method does not work if context is not taken in despite it not using it.
    """

    gravatar_default = 'blank'

    if user:
        if not first_name and hasattr(user, 'first_name'):
            first_name = user.first_name

        if not last_name and hasattr(user, 'last_name'):
            last_name = user.last_name

    if not initials:
        if first_name and last_name:
            initials = '{} {}'.format(first_name[0], last_name[0])
        elif first_name:
            initials = '{}'.format(first_name[0])
        elif last_name:
            initials = '{}'.format(last_name[0])
        else:
            gravatar_default = 'mp'

    profile_url = get_avatar_url(
        context,
        size=size,
        user=user,
        email=email,
        default=gravatar_default
    )

    return {
        'initials': initials or '',
        'profile_url': profile_url,
        'title': "{} {}".format(first_name or '', last_name or '').strip(),
    }

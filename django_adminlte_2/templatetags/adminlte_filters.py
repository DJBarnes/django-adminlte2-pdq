"""
Django AdminLTE2 Template Filters

Various filters that can be used to work with a django form to add missing
attributes that the user would like the form fields to have.
"""
from django import template
import json
register = template.Library()


@register.filter('fieldtype')
def fieldtype(field):
    """
    Get a string representation of what fieldtype a given field is.
    """
    return field.field.widget.__class__.__name__


@register.filter('with_attrs')
def with_attrs(field, attrs_as_json=None):
    """
    Add generic attributes to a form field and return the form field so filters can be chained.

    The attrs to add must be in the form of json

    Example:
        {% load adminlte_filters %}
        {% for field in form %}
            {% field|with_attrs:'{"attribute-1":"value-1", "attribute-2":"value-2"}' %}
            {% field %}
        {% endfor %}

        Which will update the form field to look like the following:

        <input type="text" name="field" attribute-1="value-1" attribute-2="value-2" id="id_field" />
    """
    attrs_as_json = attrs_as_json or {}
    attrs = field.field.widget.attrs
    data_attrs = json.loads(attrs_as_json)
    for key, value in data_attrs.items():
        attrs[f'{key}'] = value
    field.field.widget.attrs = {**field.field.widget.attrs, **attrs}
    return field


@register.filter('with_class')
def with_class(field, class_name=''):
    """
    Add a class attribute to a form field and return the form field so filters can be chained.

    Example:
        {% load adminlte_filters %}
        {% for field in form %}
            {% field|with_class:'my-added-class' %}
            {% field %}
        {% endfor %}

        Which will update the form field to look like the following:

        <input type="text" name="field" class="my-added-class" id="id_field" />
    """
    if not field:
        return field
    attrs = field.field.widget.attrs
    current_class_list = attrs.get('class', '').split()
    current_class_list.append(class_name)
    attrs['class'] = " ".join(current_class_list)
    field.field.widget.attrs = {**field.field.widget.attrs, **attrs}
    return field


@register.filter('with_data')
def with_data(field, data_attrs_json=None):
    """
    Add data attributes to a form field and return the form field so filters can be chained.

    The data fields to add must be in the form of json

    Example:
        {% load adminlte_filters %}
        {% for field in form %}
            {% field|with_data:'{"attribute-1":"value-1", "attribute-2":"value-2"}' %}
            {% field %}
        {% endfor %}

        Which will update the form field to look like the following:

        <input
            type="text"
            name="field"
            data-attribute-1="value-1"
            data-attribute-2="value-2"
            id="id_field"
        />
    """
    data_attrs_json = data_attrs_json or {}
    attrs = field.field.widget.attrs
    data_attrs = json.loads(data_attrs_json)
    for key, value in data_attrs.items():
        attrs[f'data-{key}'] = value
    field.field.widget.attrs = {**field.field.widget.attrs, **attrs}
    return field


@register.filter('with_placeholder')
def with_placeholder(field, placeholder=None):
    """
    Add data attributes to a form field and return the form field so filters can be chained.

    Example:
        {% load adminlte_filters %}
        {% for field in form %}
            {% field|with_placeholder 'My Placeholder Text' %}
            {% field %}
        {% endfor %}

        Which will update the form field to look like the following:

        <input type="text" name="field" placeholder="My Placeholder Text" id="id_field" />
    """
    # Default placeholder to field.label if the widget does not already have
    # a placeholder, and a value was not sent to the method.
    # Assume that if a value for placeholder was sent in, we are using it.
    if not placeholder and 'placeholder' not in field.field.widget.attrs:
        placeholder = field.label

    if placeholder:
        attrs = field.field.widget.attrs
        attrs['placeholder'] = placeholder
        field.field.widget.attrs = {**field.field.widget.attrs, **attrs}

    return field


@register.filter('dir')
def directory(field):
    """
    Return the result of calling dir on an object.
    """
    return dir(field)


@register.filter('dictionary')
def dictionary(field):
    """
    Return the result of calling __dict__ on an object.
    """
    return field.__dict__


@register.filter('unsnake')
def unsnake(field):
    """
    Return a string that converts underscore to spaces and capitalizes first letter.
    """
    return str(field).replace('_', ' ').capitalize()


@register.filter('unslugify')
def unslugify(field):
    """
    Return a string that converts dash to spaces and capitalizes first letter.
    """
    return str(field).replace('-', ' ').capitalize()

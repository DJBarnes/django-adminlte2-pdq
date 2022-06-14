Template Filters
****************

This package includes some template filters that are designed to add some
useful features to any project.

To use any of the following template filters you first need to load them at the
top of your template.

.. code:: html+django

    {% load adminlte_filters %}


----


fieldtype
=========

Get a string representation of what field type a given field is.

:param field: Form Field to get the type of.
:return: String representation of form field type.

**Example:**

.. code:: html+django

    {% fieldtype field %}


with_attrs
==========

Add generic attributes to a form field and return the form field so filters can
be chained.

:param field: Form field to add attributes to.
:param attrs_as_json: The attrs to add to the field.
 Must be in the form of json. Defaults to None.
:return: Field that was passed in with attrs added.

**Example:**

.. code:: html+django

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|with_attrs:'{"attribute-1":"value-1", "attribute-2":"value-2"}' %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input type="text" name="field" attribute-1="value-1" attribute-2="value-2" id="id_field" />


with_class
==========

Add a class attribute to a form field and return the form field so filters can
be chained.

:param field: Form field to add attributes to.
:param class_name: Class name to add to add to the field.
 Defaults to blank string.
:return: Field that was passed in with classes added.

**Example:**

.. code:: html+django

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|with_class:'my-added-class' %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input type="text" name="field" class="my-added-class" id="id_field" />


with_data
=========

Add data attributes to a form field and return the form field so filters can be
chained.

:param field: Form field to add data attributes to.
:param data_attrs_json: The data fields to add. Must be in the form of json.
 Defaults to None.
:return: Field that was passed in with data attributes added.

**Example:**

.. code:: html+django

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|with_data:'{"attribute-1":"value-1", "attribute-2":"value-2"}' %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input
        type="text"
        name="field"
        data-attribute-1="value-1"
        data-attribute-2="value-2"
        id="id_field"
    />


with_placeholder
================

Add placeholder to a form field and return the form field so filters can be
chained.

:param field: Form field to add placeholder to.
:param placeholder: Placeholder text to use.
 Defaults to fields label if nothing provided.
:return: Field that was passed in with placeholder added.

**Example:**

.. code:: html+django

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|with_placeholder 'My Placeholder Text' %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input
        type="text"
        name="field"
        placeholder="My Placeholder Text"
        id="id_field"
    />


directory
=========

Return the result of calling dir on an object.

:param field: Form field to run dir on.
:return: dir of the field passed in.

**Example:**

.. code:: html+django

    {% directory field %}


dictionary
==========

Return the result of calling __dict__ on an object.

:param field: Form field to run __dict__ on.
:return: __dict__ of the field passed in.

**Example:**

.. code:: html+django

    {% dictionary field %}


unsnake
=======

Return a string that converts underscore to spaces and capitalizes first
letter.

:param field: Form field to unsnake.
:return: unsnaked string of the field passed in.

**Example:**

.. code:: html+django

    {% unsnake field %}


unslugify
=========

Return a string that converts dash to spaces and capitalizes first letter.

:param field: Form field to unslugify.
:return: dir of the field passed in.

**Example:**

.. code:: html+django

    {% unslugify field %}

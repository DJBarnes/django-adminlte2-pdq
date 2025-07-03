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

    {{ field|fieldtype }}


with_attrs
==========

Add generic attributes to a form field and return the form field so filters can
be chained.

:param field: Form field to add attributes to.
:param attrs_as_json: The attrs to add to the field.
 Must be in the form of JSON. Defaults to None.
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

Add a ``class`` attribute to a form field and return the form field so filters can
be chained.

:param field: Form field to add attributes to.
:param class_name: Class name to add to the field.
 Defaults to a blank string.
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
:param data_attrs_json: The data fields to add. Must be in the form of JSON.
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

Add ``placeholder`` to a form field and return the form field so filters can be
chained.

:param field: Form field to add the placeholder to.
:param placeholder: Placeholder text to use.
 Defaults to the label of the field if nothing is provided.
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


with_list
=========

Add ``list`` attribute to a form field and return the form field so filters can be chained.
This is most commonly used when making a datalist.
This will not automatically create the datalist elements.
It will only add the list attribute to the element with the name provided.

:param field: Form field to add attributes to.
:param name: The datalist name.
 Defaults to None.
:return: Field that was passed in with list attribute added.

**Example:**

.. code:: html+django

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|with_list:"my_awesome_list" %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input
        type="text"
        name="field"
        list="my_awesome_list"
        id="id_field"
    />

with_pattern
============

Add ``pattern`` attribute to a form field and return the form field so filters can be chained.

.. warning::

    Unfortunately, the Django template engine can't handle parsing a string
    regex passed to this filter. Therefore, the regex string needs to be stored
    in a variable that can be sent to the filter.

:param field: Form field to add attributes to.
:param pattern: The JavaScript regex pattern to use.
 Defaults to ``r"\([0-9]{3}\) [0-9]{3}-[0-9]{4}"`` if value not passed.
:return: Field that was passed in with pattern attribute added.

**Example:**

.. code:: html+django

    # Assuming the field has a property called pattern with a string value
    # that is the needed regex: "\([0-9]{3}\) [0-9]{3}-[0-9]{4}"
    # We can send that variable to the filter.

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|with_pattern:field.pattern %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input
        type="tel"
        name="field"
        pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
        id="id_field"
    />


with_inputmask
==============

Add an inputmask data attribute to a form field and return the form field so filters can be chained.

This inputmask is meant to work with the
`Inputmask <https://github.com/RobinHerbots/Inputmask>`_
library. More information including how to form masks can be found on the
`Inputmask <https://github.com/RobinHerbots/Inputmask>`_
site.

.. note::

    Depending on the complexity of inputmask, the Django template engine may
    not be able to handle parsing the mask if it is provided as a string right
    inside the template.
    If this is the case, the inputmask will need to be stored in a variable
    where the variable can be sent to the filter.

:param field: Form field to add attributes to.
:param inputmask: The inputmask pattern to use.
 Defaults to ``"(999) 999-9999"`` if value not passed.
:return: Field that was passed in with an inputmask data attribute added.

**Example:**

.. code:: html+django

    # Assuming the field has a property called pattern with a string value
    # that is the needed regex: "\([0-9]{3}\) [0-9]{3}-[0-9]{4}"
    # We can send that variable to the filter.

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|with_inputmask:'(999) 999-9999' %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input
        type="tel"
        name="field"
        data-inputmask="'mask':'(999) 999-9999'"
        id="id_field"
    />


with_min
========

Add ``min`` attribute to a form field and return the form field so filters can be chained.

:param field: Form field to add attributes to.
:param min_val: The min value to use.
 Defaults to 0 if value not passed.
:return: Field that was passed in with min attribute added.

**Example:**

.. code:: html+django

    # Assuming that the field has a range_min_max property and it is set to the
    # following: {'min':5, 'max':9}

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|with_min:5 %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input type="range" name="field" min="5" id="id_field" />


with_max
========

Add ``max`` attribute to a form field and return the form field so filters can be chained.

:param field: Form field to add attributes to.
:param max_val: The max value to use.
 Defaults to 100 if value not passed.
:return: Field that was passed in with max attribute added.

**Example:**

.. code:: html+django

    # Assuming that the field has a range_min_max property and it is set to the
    # following: {'min':5, 'max':9}

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|with_max:9 %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input type="range" name="field" max="9" id="id_field" />


with_input_type
===============

Change widget input_type to the passed value.

:param field: Form field to change type on.
:return: Field that was passed in with input_type changed to the passed value.

**Example:**

.. code:: html+django

    {% load adminlte_filters %}
    {% for field in form %}
        {% field|as_input_type:'date' %}
        {% field %}
    {% endfor %}

Which will update the form field to look like the following:

.. code:: html

    <input type="date" name="field" id="id_field" />


directory
=========

Return the result of calling dir on an object.

:param field: Form field to run dir on.
:return: dir of the field passed in.

**Example:**

.. code:: html+django

    {{ field|directory }}


dictionary
==========

Return the result of calling __dict__ on an object.

:param field: Form field to run __dict__ on.
:return: __dict__ of the field passed in.

**Example:**

.. code:: html+django

    {{ field|dictionary }}


unsnake
=======

Return a string that converts underscore to spaces and capitalizes first
letter.

:param field: Form field to unsnake.
:return: unsnaked string of the field passed in.

**Example:**

.. code:: html+django

    {{ my_snake|unsnake }}


unslugify
=========

Return a string that converts dash to spaces and capitalizes the first letter.

:param field: Form field to unslugify.
:return: dir of the field passed in.

**Example:**

.. code:: html+django

    {{ my_slug|unslugify }}


dict_get
========

Return value for a dict key or None if key does not exist.

:param dict_instance: Dictionary to retrieve the value from with `get`.
:param key: Key to use when attempting to `get` the value.
:return: Value for the dict key or None if key does not exist.

**Example:**

.. code:: html+django

    {{ my_dict|dict_get:my_key_var }}


multiply
========

Return result of multiplying two values. Same as python's `*` operator.

:param a: First value in multiplication operation.
:param b: Second value in multiplication operation.
:return: Result of the multiplication operation.

**Example:**

.. code:: html+django

    {{ my_first_num|multiply:my_second_num }}


divide
======

Return result of dividing the first value by the second. Same as python's `/` operator.

:param a: Dividend in the division operation.
:param b: Divisor in the division operation.
:return: Result of the division operation.

**Example:**

.. code:: html+django

    {{ my_first_num|divide:my_second_num }}


modulo
======

Return remainder after dividing the first value by the second. Same as python's `%` operator.

:param a: Dividend in the modulo operation.
:param b: Division in the modulo operation.
:return: Result of the modulo operation.

**Example:**

.. code:: html+django

    {{ my_first_num|modulo:my_second_num }}

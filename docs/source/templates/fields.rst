Fields
******

There are no additional fields provided by this package.
However, there are some :ref:`templates/fields:Enhancements` to existing
`Django Fields <https://docs.djangoproject.com/en/dev/ref/forms/fields/>`_
as well as a few :ref:`templates/fields:Text Field Properties` that can be set
on a django field to add additional rendered functionality.
Those enhancements and properties are explained below.

.. warning::

    Some of the enhancements listed here might not be fully supported in all
    browsers yet. However, as time moves on, adoption should increase.

----

Enhancements
============

DateTimeField
-------------
Any `DateTimeField <https://docs.djangoproject.com/en/dev/ref/forms/fields/#datetimefield>`_
will be rendered out with the input type set to
``datetime-local``, which will allow an automatic datetime picker widget
provided by the browser per the HTML5 spec.



DateField
---------
Any `DateField <https://docs.djangoproject.com/en/dev/ref/forms/fields/#datefield>`_
will be rendered out with the input type set to
``date``, which will allow an automatic date picker widget
provided by the browser per the HTML5 spec.



TimeField
---------
Any `TimeField <https://docs.djangoproject.com/en/dev/ref/forms/fields/#timefield>`_
will be rendered out with the input type set to
``time``, which will allow an automatic time picker widget
provided by the browser per the HTML5 spec.


----


Text Field Properties
=====================

With HTML5 there are a lot of use cases for the input element that accepts
text. Django handles some of these for us. Such as
EmailField and
URLField.
However, there are some other types that Django does not support out of the box.
Rather than making a whole new field that would have to be imported from this
package rather than the default Django forms module, we choose to do some extra
processing on a standard TextField if you set a specific property on the form
field. This extra processing will make the TextField behave with some extra
added functionality.

phone_info
----------

If you would like to make a text field render as a phone input, you can add a
``phone_info`` property defined as a dictionary with keys ``inputmask`` and
``pattern``.
This property will make the field render with both
an inputmask and regex phone pattern to use as validation.

The ``pattern`` key will have a value that is a JavaScript regular expression
that the entered phone number must pass in order to be submitted.
More information about ``pattern`` can be found via the
`Mozilla Pattern Documentation <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/tel#pattern>`_

The ``inputmask`` is specified as a string.
Information about making a valid format can be found at the repository for
`Inputmask <https://github.com/RobinHerbots/Inputmask>`_.

.. warning::

    The pattern and inputmask should not be a replacement for server-side
    validation. You should still use a clean method on the phone field
    server-side to ensure that the field does in fact have a correct value.
    The enhancements provided by this property are all client-side and can be
    circumvented. Thus it cannot be fully trusted to be accurate.

.. note::

    There are two examples below. One sets the property in the form class.
    The other in the View class. You should choose one way or the other.
    You do **NOT** need to set the property in both locations.


Setting phone_info in a Form class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**forms.py**

.. code:: python

    class SampleForm(forms.Form):
        """Sample Form with phone field type"""
        sample_phone = forms.CharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self['sample_phone'].phone_info = {
                'pattern': r'\([0-9]{3}\) [0-9]{3}-[0-9]{4}',
                'inputmask': '(999) 999-9999'
            }

Setting phone_info in a View class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**views.py**

.. code:: python

    form = SampleForm()
    form['sample_phone'].phone_info = {
        'pattern': r'\([0-9]{3}\) [0-9]{3}-[0-9]{4}',
        'inputmask': '(999) 999-9999'
    }


range_min_max
-------------

If you would like to make a text field render as a range input, you can add a
``range_min_max`` property defined as a dictionary with keys ``min`` and
``max``.
This property will make the field render with both a min and max value
that can be selected via the range.

* The ``min`` key will provide the lowest value that can be submitted via the
  input.
  More information about ``min`` can be found via the
  `Mozilla Min Range Documentation <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range#min>`_.

* The ``max`` key will provide the highest value that can be submitted via the
  input.
  More information about ``max`` can be found via the
  `Mozilla Max Range Documentation <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range#max>`_.

.. note::

    There are two examples below. One sets the property in the form class.
    The other in the View class. You should choose one way or the other.
    You do **NOT** need to set the property in both locations.


Setting range_min_max in a Form class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**forms.py**

.. code:: python

    class SampleForm(forms.Form):
        """Sample Form with range field type"""
        sample_range = forms.CharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self['sample_range'].range_min_max={'min':5, 'max':9}

Setting range_min_max in a View class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**views.py**

.. code:: python

    form = SampleForm()
    form['sample_range'].range_min_max={'min':5, 'max':9}

is_color
--------

If you would like to make a text field render as a color input, you can add a
``is_color`` property with a value of ``True``.
This property will make the field render as a color selector.
More information about ``color`` can be found via the
`Mozilla Color Documentation <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/color>`_.

.. note::

    There are two examples below. One sets the property in the form class.
    The other in the View class. You should choose one way or the other.
    You do **NOT** need to set the property in both locations.


Setting is_color in a Form class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**forms.py**

.. code:: python

    class SampleForm(forms.Form):
        """Sample Form with color field type"""
        sample_color = forms.CharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self['sample_color'].is_color = True

Setting is_color in a View class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**views.py**

.. code:: python

    form = SampleForm()
    form['sample_color'].is_color = True

datalist
--------

If you would like add a datalist to a text field, you can add a
``datalist`` property with a value of dictionary with keys ``name`` and
``data``.

* The ``name`` key should define the name of the datalist that
  will be used both as the value for the list attribute and the id in the
  rendered datalist.

* The ``data`` key should define the data for the datalist.
  This should be a list of values.

.. note::

    This property can be applied to any text field. This includes but is not
    limited to:

    * text
    * email
    * url
    * phone
    * range
    * color

    More information about how a datalist will work with the particular text
    input you have can be found at the
    `Mozilla Datalist Documentation <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist>`_.

.. note::

    There are two examples below. One sets the property in the form class.
    The other in the View class. You should choose one way or the other.
    You do **NOT** need to set the property in both locations.


Setting datalist in a Form class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**forms.py**

.. code:: python

    class SampleForm(forms.Form):
        """Sample Form with range field type"""
        sample_text = forms.CharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self['sample_text'].datalist={
                'name':'my_fancy_datalist',
                'data': [
                    'My First Option',
                    'My Final Option',
                ],
            }

Setting datalist in a View class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**views.py**

.. code:: python

    form = SampleForm()
    form['sample_text'].datalist={
        'name':'my_fancy_datalist',
        'data': [
            'My First Option',
            'My Final Option',
        ],
    }

Additional Datalist Examples
----------------------------

It is also possible to combine the work of adding a datalist with one of the
other properties to enhance the field further. In the below examples we are
using the datalist on the range input to add tickmarks to the range input at
the values in the datalist. As you can see, it is only a matter of setting
both properties on the field.

.. note::

    There are two examples below. One sets the property in the form class.
    The other in the View class. You should choose one way or the other.
    You do **NOT** need to set the property in both locations.


Setting datalist and range_min_max in a Form class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**forms.py**

.. code:: python

    class SampleForm(forms.Form):
        """Sample Form with range field type"""
        sample_range = forms.CharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self['sample_range'].range_min_max={'min':5, 'max':9}
            self['sample_range'].datalist={
                'name':'my_fancy_datalist',
                'data': [5, 7, 9],
            }

Setting datalist and range_min_max in a View class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**views.py**

.. code:: python

    form = SampleForm()
    form['sample_range'].range_min_max={'min':5, 'max':9}
    form['sample_range'].datalist={
        'name':'my_fancy_datalist',
        'data': [5, 7, 9],
    }


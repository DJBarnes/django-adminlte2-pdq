Templates
*********

This package comes with a lot of templates that are used right out of the box.
Any and all of these templates can be overridden to customize the look and feel
of the site. Rather than listing out every single file and every single block
within those files that can overridden, it is preferable that you just
reference the files yourself to see what can be overridden. The files can be
found on `GitHub <https://github.com/DJBarnes/django-adminlte-2/tree/master/django_adminlte_2/templates>`_.

For general overriding guidance, see the below instructions.

1. Override and update blocks in base.html to customize the layout further
    1. Create ``adminlte2/base.html`` in one of your django projects template
       folders
    2. Extend the packages default base.html by adding the following line to
       the file created above.

       .. code:: html+django

           {% extends "adminlte2/base.html" %}

    3. Override the skin class to set the color theme of the site by adding the
       following line to the file created above.
       Valid values can be found here: https://adminlte.io/docs/2.4/layout

       .. code:: html+django

           {% block skin_class %}skin-blue{% endblock skin_class %}

    4. Optionally override any other template blocks that you would like to
       either remove or change the implementation of

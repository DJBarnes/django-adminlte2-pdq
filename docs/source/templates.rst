Templates
=========

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

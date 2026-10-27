// Bridge jQuery UI button to `uibutton`, so it does not conflict with Bootstrap's `button` plugin.
$.widget.bridge('uibutton', $.ui.button);

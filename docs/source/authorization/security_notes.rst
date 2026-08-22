Security Notes
**************

As a general rule, there's no such thing as being **too** security-minded.

In fact, that's a large reason why this package started in the first place.
Having good "default handling" makes it harder to forget to secure any given page.
And by condensing logic into a few decorators/mixins that are easy to call, it's harder for
developers to be lazy and think "eh I'll do it later."

With that said, this package's out-of-the-box behavior generally tries to match Django's default
behavior.
This ensures that developers are not confused by unexpected behavior when first implementing this
package.

But Django's defaults are not necessarily the most secure.
In fact, when given the option, Django tends to choose "easier initial development" over
"more secure."

So below are some recommended configurations, to immediately harden your site without much
additional work.


.. note::

    Implementing these means that overall site default behavior **will** change.

    Make sure you read the package documentation to understand how expected
    functionality will change prior to updating project settings!


Choosing a More Secure Auth Policy
==================================

As mentioned in :doc:`../authorization/overview`, the default package Auth Policy is "Loose" mode.

This matches Django's general handling, but is overall less secure, as any user can access any
view by default.


As such, we strongly recommend switching to :ref:`authorization/policies:strict policy` or
at least :ref:`authorization/policies:login required`, for an immediate boost to initial security.


Preventing Url Sniffing
=======================

The value of this one may depend on the nature of your site.

If most pages are already meant for the general public, then this may not be very applicable.
However, if your site is for a business that wants to keep information private, then you may want
to consider preventing Url Sniffing.

Url Sniffing can be used in things such as phishing attacks, where a malicious third-party user
may start off by seeing what information they can gather just by accessing the site.

When sniffing around for Urls, the malicious user may enter url paths that they believe may or may
not exist on the site, experimenting to see if they can determine a way to tell what paths are
valid.


The default handling for this package will allow exactly that.
Again, this is to match Django's out-of-the-box behavior as closely as possible.

However, AdminLtePDQ has some settings which can easily prevent such behavior.


Disabling 403/404 Info Messages in Production
---------------------------------------------

When using AdminLtePDQ, a user experiencing a 403/404 page will be redirected to a "safe" location
as defined in the settings.
This is defined by the `HOME_ROUTE` setting.

When experiencing such a redirect, debug messages will display to the user upon landing on the
redirect page.

These can be incredibly helpful for development, but may not be desired for production.

These messages can be modified or disabled, via the following settings:
<LIST SETTINGS HERE>


Disabling the "Next" URL
------------------------

Similar to above, if a user is not authenticated and redirected to the login screen, they will
receive a "next=<location>" appended to the end of the URL.

This can also be used to sniff out what urls are valid and which are not.

To disable this handling, see the <SETTING HERE>.

Alternatively, if you always want users to redirect to a specific page on login, you can use the
<SETTING HERE>, which will also prevent sniffing.

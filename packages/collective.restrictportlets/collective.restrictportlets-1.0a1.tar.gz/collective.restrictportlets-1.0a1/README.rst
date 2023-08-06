.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

===========================
collective.restrictportlets
===========================

This packages allows you to restrict the available portlets that non-Managers can add.

Features
--------

- On any page where portlets can be added, the product checks a list of portlets that are restricted to only Managers.
  This includes the personal dashboard.

- There is a control panel for selecting which portlets to disallow for non-Managers.

.. image:: https://raw.githubusercontent.com/collective/collective.restrictportlets/master/docs/controlpanel.png


Compatibility
-------------

This package is tested on Plone 4.3 and 5.0.

It should be fine for Plone 4.1 and 4.2 as well:

- It patches a method from ``plone.portlets`` that has not changed since version 2.0 (Plone 4.0).

- We need ``plone.app.registry`` for our setting and the control panel, so this means Plone 4.1.

The most important part of this package is a small `monkey patch <https://github.com/collective/collective.restrictportlets/blob/master/src/collective/restrictportlets/patches.py>`_ for ``plone.portlets.manager.PortletManager.getAddablePortletTypes``.
If you have other code that patches this, it may not work.


Testing
-------

This package is tested with Travis:

.. image:: https://secure.travis-ci.org/collective/collective.restrictportlets.png
    :target: http://travis-ci.org/collective/collective.restrictportlets


Default
-------

After you install the product in the Plone add-ons control panel, by default these portlets are restricted:

- Classic portlet

- Login portlet

You can make them available again in the *Restrict portlets* control panel.


Translations
------------

This product has been translated into:

- Dutch (Maurits van Rees)


Installation
------------

Install collective.restrictportlets by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.restrictportlets


and then running ``bin/buildout``.
Now you can activate it in the add-ons control panel and configure it in the *Restrict portlets* control panel.


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.restrictportlets/issues
- Source Code: https://github.com/collective/collective.restrictportlets


License
-------

The project is licensed under the GPLv2.


Sponsorship
-----------

Work on collective.restrictportlets has been made possible by The Flemish Environment Agency, or VMM.
See https://www.vmm.be.
VMM operates as an agency of the Flemish government for a better environment in Flanders.
Flanders is one of the three Belgian regions with its own government, parliament and administration.
The other two are the Brussels-Capital Region and the Walloon Region.


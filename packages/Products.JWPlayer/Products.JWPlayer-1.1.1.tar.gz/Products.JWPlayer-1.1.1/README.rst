==============================================================================
Products.JWPlayer
==============================================================================

This extension helps you to play videos on your plone site (Plone 4.3.x) using a very basic setup of jwplayer.
When inserting a video, you can choose to use a self-hosted jwplayer library or a cloud based library.
Video is inserted into content only through the TinyMCE editor. So the Products.TinyMCE extension is required to use this extension.

Features
--------

- Play videos on your plone site (Plone 4.3.x) using `jwplayer <https://jwplayer.com>`_
- Possibility to use self-hosted or cloud based jwplayer.
- TinyMCE editor integration (only way to insert video in content)
- Configuration flexibility for the JWPlayer.


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online `here <https://github.com/cyriltata/Products.JWPlayer/blob/master/docs/index.rst>`_


Translations
------------

This product has been translated into

- German


Installation
------------

Install Products.JWPlayer by adding it to your buildout::

    [buildout]

    ...

    eggs =
        Products.JWPlayer


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/cyriltata/Products.JWPlayer/issues
- Source Code: https://github.com/cyriltata/Products.JWPlayer/
- Documentation: https://github.com/cyriltata/Products.JWPlayer/blob/master/docs/index.rst


Support
-------

If you are having issues, please let us know at cyril,tata@gmail.com


License
-------

The project is licensed under the GPLv2.

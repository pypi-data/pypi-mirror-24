.. image:: http://pybee.org/project/projects/tools/briefcase/briefcase.png
    :width: 72px
    :target: https://pybee.org/briefcase

Briefcase
=========

.. image:: https://img.shields.io/pypi/pyversions/briefcase.svg
    :target: https://pypi.python.org/pypi/briefcase

.. image:: https://img.shields.io/pypi/v/briefcase.svg
    :target: https://pypi.python.org/pypi/briefcase

.. image:: https://img.shields.io/pypi/status/briefcase.svg
    :target: https://pypi.python.org/pypi/briefcase

.. image:: https://img.shields.io/pypi/l/briefcase.svg
    :target: https://github.com/pybee/briefcase/blob/master/LICENSE

.. image:: https://beekeeper.herokuapp.com/projects/pybee/waggle/shield
    :target: https://beekeeper.herokuapp.com/projects/pybee/waggle

.. image:: https://badges.gitter.im/pybee/general.svg
    :target: https://gitter.im/pybee/general

Tools to support converting a Python project into a standalone native
application.

Quickstart
----------

In your virtualenv, install Briefcase::

    $ pip install briefcase

Then, add extra options to your ``setup.py`` file to provide the
app-specific properties of your app. Settings that are applicable
to any app can be set under the ``app`` key; platform
specific settings can be specified using a platform key::

    setup(
        ...
        options={
            'app': {
                'formal_name': 'My First App',
                'bundle': 'org.example',
            },
            'macos': {
                'app_requires': [
                    'toga-cocoa'
                ],
                'icon': 'icons/macos',
            },
            'ios': {
                'app_requires': [
                    'toga-ios'
                ],
                'icon': 'images/ios_icon',
                'splash': 'images/ios_splash',
            },
            'android': {
                'app_requires': [
                    'toga-android'
                ],
                'icon': 'images/android_icon',
                'splash': 'images/android_splash',
            },
            'tvos': {
                'app_requires': [
                    'toga-ios'
                ]
            },
            'django': {
                'app_requires': [
                    'toga-django'
                ]
            },
        }
    )

At a minimum, you must set a ``formal_name`` key (the full, formal name for the
app) and a ``bundle`` key (the bundle identifier for the author organization -
usually a reverse domain name).

Alternatively, if you're starting from scratch, you can use `cookiecutter`_ to
generate a stub project with the required content::

    $ pip install cookiecutter
    $ cookiecutter https://github.com/pybee/briefcase-template

.. _cookiecutter: http://github.com/audreyr/cookiecutter

The ``icon`` attribute specifies the prefix of a path to a set of image files.
The name specified will be appended with a number of suffixes to construct
filenames for the various icon sizes needed on each platform. You should
provide the following files:

* On iOS:
    * ``$(icon)-180.png``, a 60x60@3x image (iPhone)
    * ``$(icon)-167.png``, an 83.5x83.5@2x image (iPad Pro)
    * ``$(icon)-152.png``, a 76x76@2x image (iPad)
    * ``$(icon)-120.png``, a 40x40@3x/60x60@2x image (iPad, iPhone)
    * ``$(icon)-87.png``, a 29x29@3x image (iPad, iPhone)
    * ``$(icon)-80.png``, a 40x40@2x image (iPad, iPhone)
    * ``$(icon)-76.png``, a 76x76 image (iPad)
    * ``$(icon)-58.png``, a 29x29@2x image (iPad)
    * ``$(icon)-40.png``, a 40x40 image (iPad)
    * ``$(icon)-29.png``, a 29x29 image (iPad)

* On Android:
    * ``$(icon)-192.png``, an xxxhdpi image (192x192)
    * ``$(icon)-144.png``, an xxhdpi image (144x144)
    * ``$(icon)-96.png``, an xhdpi image (96x96)
    * ``$(icon)-72.png``, a hdpi image (72x72)
    * ``$(icon)-48.png``, an mdpi image (48x48)
    * ``$(icon)-36.png``, an ldpi image (36x36)

* On macOS:
    * ``$(icon).icns``, a composite ICNS file containing all the required icons.

* On Windows:
    * ``$(icon).ico``, a 256x256 ico file.

* On Apple TV:
    * ``$(icon)-400-front.png``, a 400x240 image to serve as the front layer of an app icon.
    * ``$(icon)-400-middle.png``, a 400x240 image to serve as the middle layer of an app icon.
    * ``$(icon)-400-back.png``, a 400x240 image to serve as the back layer of an app icon.
    * ``$(icon)-1280-front.png``, a 1280x768 image to serve as the front layer of an app icon.
    * ``$(icon)-1280-middle.png``, a 1280x768 image to serve as the middle layer of an app icon.
    * ``$(icon)-1280-back.png``, a 1280x768 image to serve as the back layer of an app icon.
    * ``$(icon)-1920.png``, a 1920x720 image for the top shelf.

If a file cannot be found, an larger icon will be substituted (if available).
If a file still cannot be found, the default briefcase icon will be used.

On Apple TV, the three provided images will be used as three visual layers of
a single app icon, producing a 3D effect. As an alternative to providing a
``-front``,  ``-middle`` and ``-back`` variant, you can provide a single
``$(icon)-(size).png``, which will be used for all three layers.

The ``splash`` attribute specifies a launch image to display while the app is
initially loading. It uses the same suffix approach as image icons. You should
provide the following files:

* On iOS:
    * ``$(splash)-2048x1536.png``, a 1024x786@2x landscape image (iPad)
    * ``$(splash)-1536x2048.png``, a 768x1024@2x portrait image (iPad)
    * ``$(splash)-1024x768.png``, a 1024x768 landscape image (iPad)
    * ``$(splash)-768x1024.png``, a 768x1024 landscape image (iPad)
    * ``$(splash)-640x1136.png``, a 320x568@2x portrait image (new iPhone)
    * ``$(splash)-640x960.png``, a 320x480@2x portrait image (old iPhone)

* On Apple TV:
    * ``$(splash)-1920x1080.icns``, a 1920x1080 landscape image

* On Android:
    * ``$(splash)-1280×1920.png``, an xxxhdpi (1280×1920) image
    * ``$(splash)-960×1440.png``, an xxhdpi (960×1440) image
    * ``$(splash)-640×960.png``, an xhdpi (640×960) image
    * ``$(splash)-480x720.png``, a hdpi (480x720) image
    * ``$(splash)-320×480.png``, an mdpi (320×480) image
    * ``$(splash)-240×320.png``, an ldpi (240×320) image

If an image cannot be found, the default briefcase image will be used.

Then, you can invoke ``briefcase``, using::

    $ python setup.py macos

to create a macOS app; or::

    $ python setup.py windows

to create an Windows app; or::

    $ python setup.py linux

to create an Linux app; or::

    $ python setup.py ios

to create an iOS app; or::

    $ python setup.py android

to create an Android app; or::

    $ python setup.py tvos

to create an tvOS app.

You can also use the ``-b`` (or ``--build``) argument to automatically
perform any compilation step required; or use ``-s`` (``--start``) to
start the application.

Documentation
-------------

Documentation for Briefcase can be found on `Read The Docs`_.

Community
---------

Briefcase is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `pybee/general`_ channel on Gitter.

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

Contributing
------------

If you experience problems with Briefcase, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: https://briefcase.readthedocs.io
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _pybee/general: https://gitter.im/pybee/general
.. _BeeWare Community Code of Conduct: http://pybee.org/community/behavior/
.. _log them on Github: https://github.com/pybee/briefcase/issues
.. _fork the code: https://github.com/pybee/briefcase
.. _submit a pull request: https://github.com/pybee/briefcase/pulls



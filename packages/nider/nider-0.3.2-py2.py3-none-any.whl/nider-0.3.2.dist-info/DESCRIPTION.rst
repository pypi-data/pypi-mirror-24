=====
nider
=====

.. image:: https://img.shields.io/pypi/v/nider.svg
        :target: https://pypi.python.org/pypi/nider

.. image:: https://img.shields.io/travis/pythad/nider.svg
        :target: https://travis-ci.org/pythad/nider

.. image:: https://readthedocs.org/projects/nider/badge/?version=latest
        :target: https://nider.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pythad/nider/shield.svg
     :target: https://pyup.io/repos/github/pythad/nider/
     :alt: Updates


Python package to add text to images, textures and different backgrounds


* Free software: MIT license
* Documentation: https://nider.readthedocs.io.

``nider`` is an approach to make generation of text based images simple yet flexible. Creating of an image is as simple as describing units you want to be rendered to the image and choosing a method that will be used for drawing.

************
Installation
************

.. code-block:: console

    $ pip install nider

*******
Example
*******

Creating a simple image is as easy as

.. code-block:: python

    from nider.models import Header
    from nider.models import Paragraph
    from nider.models import Linkback
    from nider.models import Content
    from nider.models import Image

    header = Header('Your super interesting title!')
    para = Paragraph('Lorem ipsum dolor sit amet.')
    linkback = Linkback('foo.com | @username')
    content = Content(para, header, linkback, padding=60)

    img = Image(content, fullpath='result.png')

    img.draw_on_bg('#212121')

***************
Featured images
***************

All of the featured images were drawn using ``nider`` package. Code used to generate them can be found `here <https://github.com/pythad/nider/tree/master/examples>`_.


Example 1
========
.. image:: https://github.com/pythad/nider/raw/master/examples/example1/result.png
        :alt: example1

Example 2
========
.. image:: https://github.com/pythad/nider/raw/master/examples/example2/result.png
        :alt: example2

Example 3
========
.. image:: https://github.com/pythad/nider/raw/master/examples/example3/result.png
        :alt: example3

Example 4
========
.. image:: https://github.com/pythad/nider/raw/master/examples/example4/result.png
        :alt: example4


=======
History
=======

0.1.0 (2017-07-27)
------------------

* First release on PyPI.


0.2.0 (2017-08-12)
------------------

* Added ``PIL.ImageEnhance`` and ``PIL.ImageFilter`` built-in support
* Enabled auto color generation for unit colors


0.3.0 (2017-08-17)
------------------

* Dropped shadow support for units
* Added outline support for units
* Made unit's font config as a separate class



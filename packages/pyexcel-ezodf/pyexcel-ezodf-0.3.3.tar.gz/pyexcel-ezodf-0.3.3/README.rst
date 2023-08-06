EzODF.py maintained by pyexcel
----------------------------------

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/pyexcel

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-ezodf.svg?branch=master
   :target: http://travis-ci.org/pyexcel/pyexcel-ezodf

.. image:: https://codecov.io/gh/pyexcel/pyexcel-ezodf/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pyexcel/pyexcel-ezodf

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/pyexcel/Lobby

Maintenance
=============

Since `T0ha/ezodf <https://github.com/T0ha/ezodf/>`_ was not updated for too long, **pyexcel**
tries to cover up the **holiday** period until @T0ha will come back to continue. **pyexcel**
is happy to push the changes if requested.

If you are a developer and are interested in this project, please apply for co-maintenanceship.


Abstract
========

**ezodf** is a Python package to create new or open existing OpenDocument
(ODF) files to extract, add, modify or delete document data.

a simple example::

    from ezodf import newdoc, Paragraph, Heading, Sheet

    odt = newdoc(doctype='odt', filename='text.odt')
    odt.body += Heading("Chapter 1")
    odt.body += Paragraph("This is a paragraph.")
    odt.save()

    ods = newdoc(doctype='ods', filename='spreadsheet.ods')
    sheet = Sheet('SHEET', size=(10, 10))
    ods.sheets += sheet
    sheet['A1'].set_value("cell with text")
    sheet['B2'].set_value(3.141592)
    sheet['C3'].set_value(100, currency='USD')
    sheet['D4'].formula = "of:=SUM([.B2];[.C3])"
    pi = sheet[1, 1].value
    ods.save()

for more examples see: /examples folder

Dependencies
============

* lxml <http://codespeak.net/lxml/> for painless serialisation with prefix
  declaration (xlmns:prefix="global:namespace:specifier") in the root element.
  Declarations for unused prefixes are also possible.

* nose <https://nose.readthedocs.org> for testing

For CPython 2.6 compatibility:

* weakrefset <https://pypi.python.org/pypi/weakrefset> for fixing incompatibility with
  weakref module before 2.7

* unittest2 <https://pypi.python.org/pypi/unittest2> for asserts like in python 2.7+

The target platform is CPython 2.7 and CPython 3.2+, work on compability with 
CPython 2.6 is in progress.

Installation
============

You can install it via pip:

.. code-block:: bash

    $ pip install pyexcel-ezodf


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/pyexcel/pyexcel-ezodf.git
    $ cd pyexcel-ezodf
    $ python setup.py install

Documentation
=============

http://packages.python.org/ezodf

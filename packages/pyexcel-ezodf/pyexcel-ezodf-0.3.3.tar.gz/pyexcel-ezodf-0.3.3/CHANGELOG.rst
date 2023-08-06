
NEWS
====

Version 0.3.3 - 17 Auguest 2017

Package name is now changed to pyexcel-ezodf but you do not need to
change your code. You stiil import it as `ezodf`

  * `issue 1 <https://github.com/pyexcel/pyexcel-ezodf/issues/1>`_,
	stream alike object(except StringIO) cannot be handled
  * `issue 3 <https://github.com/pyexcel/pyexcel-ezodf/issues/3>`_,
    `ezodf PR 21 <https://github.com/T0ha/ezodf/pull/21>`_ license.rst -> license.txt
  * `issue 4 <https://github.com/pyexcel/pyexcel-ezodf/issues/4>`_,
    `ezodf PR 20 <https://github.com/T0ha/ezodf/pull/20>`_ cell.value_as()
  * `issue 5 <https://github.com/pyexcel/pyexcel-ezodf/issues/5>`_,
	`ezodf issue 23 <https://github.com/T0ha/ezodf/pull/23>`_
    restore the support for fodt and fods
  * `issue 6 <https://github.com/pyexcel/pyexcel-ezodf/issues/6>`_,
    `ezodf PR 17 <https://github.com/T0ha/ezodf/pull/17>`_ add Python 3.5 to test matrix
  * `PR 18 <https://github.com/T0ha/ezodf/pull/18>`_,
	Use cStringIO as default but keep StringIO as optional

Version 0.3.2 - December 2015

  * Support wheels and python3

Version 0.3.1 - December 2015

  * File-like objects utilisation improved

Version 0.3.0 - November 2014

  * Maitainer changed
  * Simple variables and user fields support added
  * Tests system changed to nose
  * Travis CI support added
  * Python 2.6 - 3.4 support added

Version 0.2.5 - Juli 2012

  * Alpha version
  * license changed to MIT license
  * development stopped - for now

Version 0.2.4 - June 2012

  * Alpha version
  * can open tables with many repeated rows/cols, 3 opening strategies are supported
  * tested: on Win7/Ubuntu 32-Bit with CPython 2.7 and CPython 3.2

Version 0.2.3 - January 2012

  * Alpha version
  * tested: on Windows7 32 Bit with CPython 2.7 and CPython 3.2

Version 0.2.2 - March 2011

  * Alpha version
  * Spreadsheet: added cell-span management
  * tested with Python 3.2 - OK
  * added tobytes() method to all document classes
  * opendoc() accept the zip-file content as 'bytes' instead of the filename
    as parameter 'filename'
  * newdoc() accept the zip-file content as 'bytes' instead of the filename
    as parameter 'template'

Version 0.2.1 - 06 February 2011

  * Alpha version
  * added basic spreadsheet support
  * Spreadsheet: added sheet, row, column and cell management

Version 0.2.0 - 18 January 2011

  * Alpha version
  * create new empty odt, ods, odp, odg file
  * added template support - can create ott, ots, otp, otg files
  * open documents - ezodf.opendoc(filename)
  * create new documents - ezdof.newdoc(doctype, filename, template)
  * Text: added Paragraph, Heading, Span, Hyperlink, List, Section objects

Version 0.1.0 - 02 January 2011

  * Pre-Alpha version
  * open/saveas ODF documents
  * modify meta data

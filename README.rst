==========
pygnutools
==========

pygnutools is an implementation of the GNU tools in pure Python. 

Work in Progress
================

So far the only implemented tool is ``find`` tool. Not even all find primaries are implemented yet.

Plugin Architecture
===================

Unlike the GNU find tool, this implementation allows plugins to be easily added. 
The plugin architecture uses setuptools entry points.

See exivfind_ as an example that provides pyfind with EXIF primaries.

.. _exivfind: https://github.com/meitham/exivfind

Difference from GNU find
========================

This tools is not and will not be fully compatable with GNU find. For example
GNU find inserts the ``-print`` automatically for you, where this tool won't.
The reason for this is GNU find is oriented around filenames, a test match will
give you back the file name that you after, where as this tool can do a lot 
more than that, such as print something from the ``context`` object that was
populated by one of the primaries.

If you're interested in printing the file names you could always do that by
explicitly provide the ``-print`` primary.

Getting Started
===============

Clone::

	git clone https://github.com/meitham/pygnutools

Install::

	cd pygnutools && python setup.py install

Run Examples::

	pyfind . -name \*.pyc -print

	pyfind some_path -iname \*.png -exec rm \{} \;


License
=======

See LICENCE file


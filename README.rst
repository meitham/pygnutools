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

See exivfind__ as an example that provides pyfind with EXIF primaries.

exivfind__: https://github.com/meitham/exivfind


Getting Started
---------------

Clone::

	git clone https://github.com/meitham/pygnutools

Install::

	cd pygnutools && python setup.py install

Run::

	find . -name \*.pyc -print

	find some_path -iname \*.png -exec rm \{} \;


License
-------

See LICENCE file


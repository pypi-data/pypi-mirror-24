====================================
Downloading and Installation
====================================

Prerequisites
~~~~~~~~~~~~~~~

This package requires Python version 2.7, 3.5, or 3.6.  It may
work with Python 2.6, 3.2, 3.3, or 3.4, but these are no longer being
tested regularly.

In addition, version 3.14 of the EPICS Channel Access library (v
3.14.8 or higher, I believe) is required.  More specifically, the
shared libraries libCom.so and libca.so (or Com.dll and ca.dll on
Windows) from *Epics Base* are required to use this module.  Using
version 3.14.12 or higher is recommended -- some of the features for
'subarray records' will only work with this 3.14.12 and higher.

For 32-bit Python on 32-bit or 64-bit Windows, pre-built DLLs from 3.14.12
(patched as of March, 2011) are included and installed so that no other
Epics installation is required to use the modules.

For 64-bit Python on 64-bit Windows, pre-built DLLs from 3.14.12.4 (patched
as of January, 2015) are also included.  Support for 64-bit Python on
Windows was new in version 3.2.4, and requires Python version 2.7.9.

For 32-bit, 64-bit Linux and 64-bit OSX binaries are also included.

If you have epics-base already installed on your machine you can
suppress installing the binaries set the env `NOLIBCA` ::

  NOLIBCA=1 pip install pyepics

You may have to set environmental variables such as PATH,
LD_LIBRARY_PATH, or DYLD_LIBRARY_PATH or using Linux tools such as
ldconfig to find the required libraries.


The Python `numpy module <http://numpy.scipy.org/>`_ is highly recommended,
though it is not strictly required. If available, it will be used to
convert EPICS waveforms values into numpy arrays.


Downloads and Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _pyepics github repository:      http://github.com/pyepics/pyepics
.. _Python Setup Tools:                http://pypi.python.org/pypi/setuptools
.. _pyepics PyPi:                           https://pypi.python.org/pypi/pyepics/3.2.5
.. _pyepics CARS downloads:       http://cars9.uchicago.edu/software/python/pyepics3/src/


The latest stable version of the PyEpics Package is 3.2.7.  Source
code kits and Windows installers can be found at either `pyepics
PyPI`_ or `pyepics CARS downloads`_ site.  With `Python Setup Tools`_
now standard for Python 2.7 and abouve, the simplest way to install
the pyepics is with::

     pip install pyepics

If you're using Anaconda, there are a few conda channels for pyepics,
including::

     conda install -c https://conda.anaconda.org/GSECARS pyepics


Getting Started, Setting up the Epics Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order for PyEpics to work at correctly, it must be able to find and load the
Channel Access dynamic library (*libca.so*, *libca.dylib*, or *ca.dll*
depending on the system).  This dynamic library needs to found at runtime.

There are a few ways to specify how to find this library:

 1. set the environmental variable ``PYEPICS_LIBCA`` to the full path of the dynamic library, for example::

     > export PYEPICS_LIBCA=/usr/local/epics/base-3.14.12.1/lib/linux-x86/libca.so

 2. set the environmental variables ``EPICS_BASE`` and  ``EPICS_HOST_ARCH``
    to point to where the library was built.   For example::

     > export EPICS_BASE=/usr/local/epics/base-3.14.12.1
     > export EPICS_HOST_ARCH=linux-x86

    will find the library at /usr/local/epics/base-3.14.12.1/lib/linux-x86/libca.so.

 3. Put the dynamic library somewhere in the Python path.  A convenient
    place might be the same ``site-packages/pyepics library`` folder as the
    python package is installed.

To find out which CA library will be used by pyepics, use:
    >>> import epics
    >>> epics.ca.find_libca()

which will print out the full path of the CA dynamic library that will be
used.


**Note for Windows users**: The needed CA DLLs (ca.dll and Com.dll) are
included in the installation kit, and should be automatically installed to
where they can be found at runtime (following rule 3 above).  If they are
not found (or another version is found that conflicts),  you should copy
them to a place where they can be found, such as the Python DLLs folder,
which might be something like ``C:\Python36\DLLs``.

For more details, especially about how to set paths for LD_LIBRARY_PATH or
DYLD_LIBRARY_PATH on Unix-like systems, see the INSTALL file.

With the Epics library loaded, it will need to be able to connect to Epics
Process Variables. Generally, these variables are provided by Epics I/O
controllers (IOCs) that are processes running on some device on the
network.   If you're connecting to PVs provided by IOCs on your local
subnet, you should have no trouble.  If trying to reach further network,
you may need to set the environmental variable ``EPICS_CA_ADDR_LIST`` to
specify which networks to search for PVs.


Testing
~~~~~~~~~~~~~

Automated, continuous unit-testing is done with the TravisCI
(https://travis-ci.org/pyepics/pyepics) for Python 2.7, 3.4, and 3.5 using
an Epics IOC running in a Docker image.  Many tests located in the `tests`
folder can also be run using the script ``tests/simulator.py`` as long as
the Epics database in ``tests/pydebug.db`` is loaded in a local IOC.  The
following systems were tested for 3.2.5 were tested locally, all with Epics
base 3.14.12.1 or higher:


+-----------+-----------------+--------------+---------------------------+
| Host OS   | Epics HOST ARCH |  Python      | Test Status               |
+===========+=================+==============+===========================+
| Linux     |  linux-x86      | 2.6   32bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+
| Linux     |  linux-x86      | 2.7.3 32bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+
| Linux     |  linux-x86_64   | 2.7.8 64bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+
| Linux     |  linux-x86_64   | 3.4.1 64bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+
| Mac OSX   |  darwin-x86     | 2.7.8 64bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+
| Windows   |  win32-x86      | 2.6.6 32bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+
| Windows   |  win32-x86      | 2.7.8 32bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+
| Windows   |  win32-x86      | 3.4.1 32bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+
| Windows   |  windows-x64    | 2.7.9 64bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+
| Windows   |  windows-x64    | 3.4.2 64bit  | pass                      |
+-----------+-----------------+--------------+---------------------------+


Testing Notes:

  1. tests involving subarrays are known to fail with Epics base earlier
     than 3.14.11.

  2. The autosave module relies on the 3rd part extension pyparsing, which
     seems to not work correctly for Python3, and has not been included in
     these tests.

  3. The wx module is not automatically tested.


Development Version
~~~~~~~~~~~~~~~~~~~~~~~~

The PyEpics module is still under active development, with enhancements and
bug-fixes are being added frequently.  All development is done through the
`pyepics github repository`_.  To get a read-only copy of the latest
version, use one of::

   git clone http://github.com/pyepics/pyepics.git
   git clone git@github.com/pyepics/pyepics.git




Getting Help
~~~~~~~~~~~~~~~~~~~~~~~~~

For questions, bug reports, feature request, please consider using the
following methods:

 1.  Send email to the Epics Tech Talk mailing list.  You can also send
     mail directly to Matt Newville <newville@cars.uchicago.ed>, but the
     mailing list has many Epics experts reading it, so someone else
     interested or knowledgeable about the topic might provide an
     answer. Since the mailing list is archived and the main mailing list
     for Epics work, a question to the mailing list has a better chance of
     helping someone else.

 2.  Create an Issue on http://github.com/pyepics/pyepics.  Though the
     github Issues seem to be intended for bug tracking, they are a fine
     way to catalog various kinds of questions and feature requests.

 3.  If you're sure you've found a bug in existing code, or have some code
     you think would be useful to add to PyEpics, and you're familiar with
     git, make a Pull Request on http://github.com/pyepics/pyepics.


License
~~~~~~~~~~~~~~~~~~~

The PyEpics source code, this documentation, and all material associated
with it are distributed under the Epics Open License:

.. include:: ../LICENSE

In plain English, this says that there is no warranty or gaurantee that the
code will actually work, but you can do anything you like with this code
except a) claim that you wrote it or b) claim that the people who did write
it endorse your use of the code.  Unless you're the US government, in which
case you can probably do whatever you want.

Acknowledgments
~~~~~~~~~~~~~~~~~~~~~~

PyEpics was originally written and is maintained by Matt Newville
<newville@cars.uchicago.ed>.  Many important contributions to the library
have come from Angus Gratton while at the Australian National University.
Several other people have provided valuable additions, suggestions, or bug
reports, which has greatly improved the quality of the library: Ken Lauer,
Robbie Clarken, Daniel Allen, Michael Abbott, Daron Chabot, Thomas Caswell,
Georg Brandl, Niklas Claesson, Jon Brinkmann, Marco Cammarata, Craig
Haskins, Pete Jemian, Andrew Johnson, Janko Kolar, Irina Kosheleva, Tim
Mooney, Eric Norum, Mark Rivers, Friedrich Schotte, Mark Vigder, Steve
Wasserman, and Glen Wright.

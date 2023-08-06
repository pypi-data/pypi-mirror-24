=======================
eudat.accounting.client
=======================

Upload accounting records to an eudat accounting server

Administrators of (storage) resources provided through the EUDAT Common Data 
Infrastructure can use this tool to conveniently report current resource 
consumption per registered resource. Accounting records are submitted per
individual resource identified by its (P)ID which is available as soon as
the resource has been registered at EUDAT's Data Project Management Tool (DPMT_).

Default settings are such that only the resource id and the consumed value 
need to be provided. The default unit is ``byte`` and the default resource 
type is set to ``storage``.
The full documentation of options supported is described in the next section.

If the tools provided here do not address your use case you can either file
a feature request on the tracker_ or use a more low-level approach as 
outlined in the `server documentation`_.

.. _DPMT: https://dp.eudat.eu
.. _tracker: https://github.com/EUDAT-DPMT/eudat.accounting.client/issues
.. _`server documentation`: https://github.com/EUDAT-DPMT/eudat.accounting.server/blob/master/README.rst#adding-records


Full documentation and API
==========================

Installation
------------

The easiest way to install the tool is via ``pip`` or ``easy_install``.
It is usually best to do this in a ``virtualenv``:

.. code:: console

  $ pip install eudat.accounting.client

Command line interface
----------------------

As a result of the above there are now two console script called 
``addRecord`` and ``iRODScollector``.
Invoke it with ``-h`` to see its usage pattern and options.

addRecord
~~~~~~~~~

.. code:: console

  $ bin/addRecord -h
  usage: addRecord [-h] [--version] [-b BASE_URL] [-u USER] [-p PASSWORD]
                   [-d DOMAIN] [-s SERVICE] [-n NUMBER] [-o OBJECT_TYPE]
                   [-k KEY] [-T TYPE] [-m MEASURE_TIME] [-C COMMENT] [-t] [-v]
                   account value [unit]

  positional arguments:
    account               account to be used. Typically the (P)ID of the
                          resource to be accounted
    value                 The value to be recorded
    unit                  The unit of measurement for the value provided.
                          Default: "byte"

  optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -b BASE_URL, --base_url BASE_URL
                          base URL of the accounting server to use. Default:
                          https://accounting.eudat.eu
    -u USER, --user USER  user id used for logging into the server. If not
                          provided it is looked up in the environment variable
                          "ACCOUNTING_USER". Default: "" - aka not set
    -p PASSWORD, --password PASSWORD
                          password used for logging into the server. If not
                          provided it is looked up in the environment variable
                          "ACCOUNTING_PW". Default: "" - aka not set
    -d DOMAIN, --domain DOMAIN
                          name of the domain holding the account. Default: eudat
    -s SERVICE, --service SERVICE
                          UID (or PID) of the registered service component
                          reporting the record. Default: "" - not set
    -n NUMBER, --number NUMBER
                          number of objects associated with this accounting
                          record. This is EUDAT specific. Default: "" - not set
    -o OBJECT_TYPE, --object_type OBJECT_TYPE
                          object type for the number of objects specified with
                          "-n". This is EUDAT specific. Default: "registered
                          objects"
    -k KEY, --key KEY     key used to refer to the record. If not set the
                          accounting server will create the key. Specifying an
                          existing key will overwrite the existing record.
                          Default: "" - not set
    -T TYPE, --type TYPE  type of the resource accounted. Default: storage
    -m MEASURE_TIME, --measure_time MEASURE_TIME
                          measurement time of the accounting record if different
                          from the current time. Default: "" - not set
    -C COMMENT, --comment COMMENT
                          arbitrary comment (goes into the meta dictionary).
                          Default: "" - not set
    -t, --test            Dry run. Don't push data to server - run only locally
                          Default: off
    -v, --verbose         return the key of the accounting record created.
                          Default: off


iRODScollector
~~~~~~~~~~~~~~

.. code:: console

  $ bin/iRODScollector -h
  usage: iRODScollector [-h] [--version] [-c CONFIGPATH] [-k KEY] [-T TYPE]
                        [-m MEASURE_TIME] [-C COMMENT] [-t] [-v]

  optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -c CONFIGPATH, --configpath CONFIGPATH
                          path to configuration file. Default:
                          "./irodscollector.cfg" (in the current working
                          directory)
    -k KEY, --key KEY     key used to refer to the record. If not set the
                          accounting server will create the key. Specifying an
                          existing key will overwrite the existing record.
                          Default: "" - not set
    -T TYPE, --type TYPE  type of the resource accounted. Default: storage
    -m MEASURE_TIME, --measure_time MEASURE_TIME
                          measurement time of the accounting record if different
                          from the current time. Default: "" - not set
    -C COMMENT, --comment COMMENT
                          arbitrary comment (goes into the meta dictionary).
                          Default: "" - not set
    -t, --test            Dry run. Don't push data to server - run only locally
                          Default: off
    -v, --verbose         return the key of the accounting record created.
                          Default: off

A template configuration file is included in the distribution and 
looks like this:

.. code:: console

  $ cat irodscollector.ini

  #
  # template of a configuration file for EUDAT's irodscollector
  #

  # section containing the logging options
  [Logging]
  log_file=eudatacct.log

  # section containing the properties to access the accounting server
  # to get statistical data and report them
  [Report]
  # base URL of the accounting server to be used
  base_url=https://accounting.eudat.eu
  # domain: either eudat or test or demo
  domain=eudat
  # uid of the corresponding registered storage resource on DPMT 
  # (same as storage_space_uuid on RCT)
  account=<insert uid here>
  # username of the provider on the accouniting server
  # owning the account specified above
  # contact dp-admin@mpcdf.mpg.de if you need one
  user=<username of provider>
  # if you have an access token from RCT already reuse that here
  password=<password or access token>
  service_uuid=<unsuported at the moment>

  # section contains the list of collections to be accounted together, replace
  # the examples with your collections, the script sums the values of all
  # collections and sends it to EUDAT's accounting service.
  [Collections]
  clist=
    /zone/some/path
    /zone/other/path

Copy this to ``irodscollector.cfg`` and adapt it to your site.
 
Most of this should be self-explaining. Note that you need to 
provide credentails for the accounting service. If you do not 
have any contact the EUDAT accounting manager.

In addition, you need to make sure that the user invoking 
this script has a suitable iRODS_ environment set up.

Basic usage information as well as error messages are logged 
to a file named ``.accounting.log`` in the current working 
directory from where ``addRecord`` has been invoked.

.. _iRODS: https://irods.org/


Developer notes
===============

Please use a ``virtualenv`` to maintain this package, but I should not need to say that.

The package can be installed directly from GitHub:

.. code:: console

  $ pip install git+git://github.com/EUDAT-DPMT/eudat.accounting.client

The code is organized in a nested namespace package, i.e., the real action
is happening in the subdirectory 

.. code:: console

  $ cd src/eudat/accounting/client
  
Start looking around there.

Run the tests (not really that meaningful so far):

.. code:: console

  $ python setup.py test
  $ python run_tests.py


Authors
=======

 - Raphael Ritz, MPCDF (main author)

 - Claudio Cacciari, CINECA (initial iRODScollector)

 - Pavel Weber, KIT (improved iRODScollector)


Links
=====

Project home page

  https://github.com/EUDAT-DPMT/eudat.accounting.client

Source code

  https://github.com/EUDAT-DPMT/eudat.accounting.client

Issues tracker

  https://github.com/EUDAT-DPMT/eudat.accounting.client/issues

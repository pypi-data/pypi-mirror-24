A Python interface to CryptoSys PKI Pro
=======================================

This is a Python interface to the **CryptoSys PKI Pro** library. 
CryptoSys PKI Pro is available from

    http://www.cryptosys.net/pki/.

Requires: Python 2 only (2.6 or above) on Windows platforms only,
CryptoSys PKI Pro v11.2 or above.


To use in Python's REPL
-----------------------

::

    >>> from cryptosyspki import *
    >>> Gen.version() # "hello world!" for CryptoSys PKI
    110200
    >>> Hash.hex_from_data('abc') # compute SHA-1 hash in hex of the string 'abc'
    'a9993e364706816aba3e25717850c26c9cd0d89d'
    >>> Hash.hex_from_data('abc', Hash.Alg.SHA256)   # same but using SHA-256
    'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
    >>> h = Hash.data('abc')   # h is a byte array
    >>> print Cnv.tohex(h)     # display the byte array in hex
    A9993E364706816ABA3E25717850C26C9CD0D89D

If you don't like ``import *`` and find ``cryptosyspki`` a bit long to
type each time, try

::

    >>> import cryptosyspki as pki
    >>> pki.Gen.version()
    110200

	
Examples
--------

Look in the file ``test\test_pki.py`` and you should find an example of use for almost every available method.
See also the main web page https://www.cryptosys.net/pki/python.html.

Tests
-----

There is a series of tests in ``test\test_pki.py``. 

The tests require certain files to exist in the current working directory and create extra files when they run.
To manage this, ``test_pki.py`` create a temporary subdirectory which is deleted automatically.
It requires a subdirectory ``work`` in the same folder
as the ``test_pki.py`` file which should contain all the required test
files, available separately in the file ``pkiPythonTestFiles.zip``. The
test function then creates a temporary subdirectory which is deleted
automatically.

::

    test/
        test_pki.py  # this module
		pkiPythonTestFiles.zip  # spare copies
        work/        # this _must_ exist
            <all required test files>
            pki.tmp.XXXXXXXX/    # created by `setup_temp_dir()`
                <copy of all required test files>
                <files created by tests>

We've tested this using the Python 2.7.12 interpreter and IDLE, 
JetBrains PyCharm Community Edition 2017.1.4, the
PyDev environment in Eclipse, and using ``py.test``.


The source code has been checked by ``flake8`` ignoring error codes
``E501,E701,E221,E222`` "line too long", "multiple statements on one
line (colon)", "multiple spaces before/after operator" (correspondence
on these issues will not be entered into!).

Changes in v11.2
----------------

* Synchronized cryptosyspki.py version number with main core module (11.2.0).
* Substantial changes to inline documentation.
* Renamed ``Rng.bytes`` to ``Rng.bytestring`` to avoid clashes with Python built-in function.
* Changed parameters in ``X509.cert_path_is_valid()`` and ``X509.get_cert_count_from_p7()``.

Contact
-------

For more information or to make suggestions, please contact us at
http://www.cryptosys.net/contact/

| David Ireland
| DI Management Services Pty Ltd
| Australia
| <www.di-mgt.com.au> <www.cryptosys.net>
| 11 August 2017

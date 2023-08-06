pyx509: X.509 Certificate and PKCS7 Parser / Verifier for Python
################################################################

This is a fork of the original project:

    pyx509 - Python library for parsing X.509
    Copyright (C) 2009-2012  CZ.NIC, z.s.p.o. (http://www.nic.cz)

Work in progress!

Description
===========

This is probably the most complete parser of X.509 certificates in python.

Code is in alpha stage! Don't use for anything sensitive. I wrote it (based on
previous work of colleagues) since there is no comprehensive python parser for
X.509 certificates. Often python programmers had to parse openssl output.

Advantages
----------

* I find it less painful to use than parsing output of 'openssl x509'
  somewhat stricter in extension parsing compared to openssl

Disadvantages
-------------

* It's slow compared to openssl (about 2.3x compared to RHEL's openssl-1.0-fips)

* Currently not very strict in what string types in RDNs it accepts

* API is still rather ugly and has no documentation yet; code is nasty at some
  places (and there's some old dangling code like pkcs7/verifier.py)


Dependencies
============

* pyasn1 >= 0.1.7


Installation
============

Install with pip::

    pip install pyx509_ph4


License
=======

LGPL v2 or later.

See LICENSE.txt.


Known bugs and quirks
=====================

* Subject alternative name doesn't show all subtypes,
  but 'DNS', 'dirName' and 'email' are supported.

* Name constraints don't distinguish among various GeneralName subtypes

* Some extensions are not shown very nicely when put in string format

* Not all extensions are supported

* String types accepted for various RDN subelements are rather too permissive

* RDN string conversion does not conform to RFC 4514

* Badly formed extensions are ignored if not marked critical

  * easy to switch to more strict behavior

  * other clients do this as well; RFC 5280 specifies behavior for unknown
    elements in extensions in appendix B.1, but does not cover all cases (e.g.
    element exists, but with string type different from spec)

TODO
====

* Cleanup: This module has it's own pyasn1 models. Look if we can
  reuse the pyasn1_modules.rfc2459 X509 cert model.
  https://github.com/etingof/pyasn1-modules/blob/master/tools/pkcs7dump.py

* Cleanup: Currently, the signature verifier does not work.


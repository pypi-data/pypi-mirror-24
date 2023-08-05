=====
PyRPM
=====

.. image:: https://travis-ci.org/02strich/pyrpm.png
   :target: https://travis-ci.org/02strich/pyrpm
.. image:: https://coveralls.io/repos/github/02strich/pyrpm/badge.svg?branch=master
   :target: https://coveralls.io/github/02strich/pyrpm?branch=master
.. image:: https://badge.fury.io/py/pyrpm-02strich.svg
   :target: https://badge.fury.io/py/pyrpm-02strich


:authors: Stefan Richter, Mário Morgado
:license: BSD

PyRPM is a pure python module to extract information from a RPM package and to create YUM metadata. Supports generation/editing YUM repositories.

Usage
-----

        >>> from pyrpm.rpm import RPM
        >>> rpm = RPM(open('package-1.0-r1.i586.rpm', 'rb') # make sure to open the file in binary mode
        >>> rpm.binary # this means that the package is a rpm and not a src.rpm
        True
        >>> rpm.header.name
        'package'
        >>> rpm.header.architecture
        'i586'
        >>> rpm.header.description
        'package description'

YUM Repository
--------------

        >>> from pyrpm.yum import YumPackage
        >>> repo = YumRepository("testrepo")
        >>> # read existing repo
        >>> repo.read()
        >>> # add package
        >>> repo.add_package(YumPackage(open(os.path.join(repo.repodir, 'tst/Eterm-0.9.3-5mdv2007.0.src.rpm'), 'rb')))
        >>> # delete package
        >>> repo.remove_package('4d9c71201f9c0d11164772600d7dadc2cad0a01ac4e472210641e242ad231b3a')
        >>> repo.save()

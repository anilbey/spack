# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPy4j(PythonPackage):
    """Enables Python programs to dynamically access arbitrary Java
    objects."""

    homepage = "https://www.py4j.org/"
    url = "https://pypi.io/packages/source/p/py4j/py4j-0.10.4.tar.gz"

    version('0.10.9', sha256='36ec57f43ff8ced260a18aa9a4e46c3500a730cac8860e259cbaa546c2b9db2f')
    version('0.10.8.1', sha256='8329bb156a0cf37be9642a2a060dbdb627b5fcb827919be65d95102daccca274')
    version('0.10.7', sha256='721189616b3a7d28212dfb2e7c6a1dd5147b03105f1fc37ff2432acd0e863fa5')
    version('0.10.6', sha256='d3e7ac7c2171c290eba87e70aa5095b7eb6d6ad34789c007c88d550d9f575083')
    version('0.10.4', sha256='406fbfdbcbbb398739f61fafd25724670a405a668eb08c1721d832eadce06aae')
    version('0.10.3', sha256='f4570108ad014dd52a65c2288418e31cb8227b5ecc39ad7fc7fe98314f7a26f2')

    depends_on('py-setuptools', type='build')

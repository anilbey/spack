# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXmltodict(PythonPackage):
    """Python module to work with XML feel like you are working with JSON"""

    homepage = "https://github.com/martinblech/xmltodict"
    git      = "https://github.com/martinblech/xmltodict.git"
    url      = "https://pypi.io/packages/source/x/xmltodict/xmltodict-0.12.0.tar.gz"

    version('0.12.0', sha256='50d8c638ed7ecb88d90561beedbf720c9b4e851a9fa6c47ebd64e99d166d8a21')

    depends_on('py-setuptools', type=('build', 'run'))

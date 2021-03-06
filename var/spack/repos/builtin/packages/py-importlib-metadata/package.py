# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImportlibMetadata(PythonPackage):
    """Read metadata from Python packages."""

    homepage = "http://importlib-metadata.readthedocs.io/"
    url      = "https://pypi.io/packages/source/i/importlib_metadata/importlib_metadata-0.23.tar.gz"

    version('1.0.0', sha256='a82ca8c109e194d7d6aee3f7531b0470dd4dd6b36ec14fd55087142a96bd55a7')
    version('0.23', sha256='aa18d7378b00b40847790e7c27e11673d7fed219354109d0e7b9e5b25dc3ad26')
    version('0.19', sha256='23d3d873e008a513952355379d93cbcab874c58f4f034ff657c7a87422fa64e8')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-zipp@0.5:', type=('build', 'run'))
    depends_on('py-pathlib2', when='^python@:3.4', type=('build', 'run'))
    depends_on('py-contextlib2', when='^python@:2.8', type=('build', 'run'))
    depends_on('py-configparser@3.5:', when='^python@:2.8', type=('build', 'run'))
    depends_on('py-packaging', type='test')

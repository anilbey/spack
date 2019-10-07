# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
import os
import tempfile


class Mysql(CMakePackage):
    """MySQL is an open source relational database management system."""

    homepage = "https://www.mysql.com/"
    url      = "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.15.tar.gz"

    version('8.0.16', sha256='8d9fe89920dc8bbbde2857b7b877ad2fa5ec2f231c68e941d484f3b72735eaea')
    version('8.0.15', sha256='bb1bca2dc2f23ee9dd395cc4db93b64561d4ac20b53be5d1dae563f7be64825e')
    version('8.0.14', sha256='bc53f4c914fb39650289700d144529121d71f38399d2d24a0f5c76e5a8abd204')
    version('8.0.13', sha256='d85eb7f98b6aa3e2c6fe38263bf40b22acb444a4ce1f4668473e9e59fb98d62e')
    version('8.0.12', sha256='69f16e20834dbc60cb28d6df7351deda323330b9de685d22415f135bcedd1b20')
    version('8.0.11', '38d5a5c1a1eeed1129fec3a999aa5efd')
    version('5.7.26', sha256='5f01d579a20199e06fcbc28f0801c3cb545a54a2863ed8634f17fe526480b9f1')
    version('5.7.25', sha256='53751c6243806103114567c1a8b6a3ec27f23c0e132f377a13ce1eb56c63723f')
    version('5.7.24', sha256='05bf0c92c6a97cf85b67fff1ac83ca7b3467aea2bf306374d727fa4f18431f87')
    version('5.7.23', sha256='0730f2d5520bfac359e9272da6c989d0006682eacfdc086a139886c0741f6c65')
    version('5.7.22', '269935a8b72dcba2c774d8d63a8bd1dd')
    version('5.7.21', sha256='fa205079c27a39c24f3485e7498dd0906a6e0b379b4f99ebc0ec38a9ec5b09b7')
    version('5.7.20', sha256='5397549bb7c238f396c123db2df4cad2191b11adf8986de7fe63bff8e2786487')
    version('5.7.19', sha256='3e51e76f93179ca7b165a7008a6cc14d56195b3aef35d26d3ac194333d291eb1')
    version('5.7.18', sha256='0b5d71ed608656cd8181d3bb0434d3e36bac192899038dbdddf5a7594aaea1a2')
    version('5.7.17', sha256='cebf23e858aee11e354c57d30de7a079754bdc2ef85eb684782458332a4b9651')
    version('5.7.16', sha256='4935b59974edb275629f6724a0fcf72265a5845faf1e30eeb50ed4b6528318a5')
    version('5.7.15', sha256='9085353143bfda59c90aa959e79a35622a22aa592e710993416e193b37eb9956')
    version('5.7.14', sha256='f7415bdac2ca8bbccd77d4f22d8a0bdd7280b065bd646a71a506b77c7a8bd169')
    version('5.7.13', sha256='50bf1a1635a61235fc43fd4876df2f77163de109372679e29c1ff8dbc38a0b87')
    version('5.7.12', sha256='32843cb6d22ab22cd2340262b53c0d6009b5bd41b1fa4102beda19635a5c1c87')
    version('5.7.11', sha256='54f8c7af87d3d8084419bde2b9f0d8970b3dada0757b015981b02f35a3681f0e')
    version('5.7.10', sha256='1ea1644884d086a23eafd8ccb04d517fbd43da3a6a06036f23c5c3a111e25c74')
    version('5.7.9',  sha256='315342f5bee1179548cecad2d776cd7758092fd2854024e60a3a5007feba34e0')
    version('5.6.44', sha256='c031c92c3f226856b09bf929d8a26b0cd8600036cb9db4e0fdf6b6f032ced336')
    version('5.6.43', sha256='1c95800bf0e1b7a19a37d37fbc5023af85c6bc0b41532433b3a886263a1673ef')
    version('5.5.62', sha256='b1e7853bc1f04aabf6771e0ad947f35ac8d237f4b35d0706d1095c9526ff99d7')

    variant('client_only', default=False,
            description='Build and install client only.')
    variant('cxxstd',
            default='98',
            values=('98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    # 5.7.X cannot be compiled client-only.
    conflicts('+client_only', when='@5.7.0:5.7.999')
    # Server code has a macro 'byte', which conflicts with C++17's
    # std::byte.
    conflicts('cxxstd=17', when='@8.0.0:~client_only')

    provides('mysql-client')

    # https://dev.mysql.com/doc/refman/8.0/en/source-installation.html

    # See CMAKE_MINIMUM_REQUIRED in CMakeLists.txt
    depends_on('cmake@3.1.0:', type='build', when='@5.7.0:5.7.999 platform=win32')
    depends_on('cmake@3.8.0:', type='build', when='@8.0.0: platform=win32')
    depends_on('cmake@3.9.2:', type='build', when='@8.0.0: platform=darwin')
    depends_on('cmake@3.4.0:', type='build', when='@8.0.0: platform=solaris')
    depends_on('cmake@2.6:', type='build', when='@:5.6.999')
    depends_on('cmake@2.8.9:', type='build', when='@5.7.0:5.7.999')
    depends_on('cmake@2.8.12:', type='build', when='@8.0.0:')

    depends_on('gmake@3.75:', type='build')

    # Each version of MySQL requires a specific version of boost
    # See BOOST_PACKAGE_NAME in cmake/boost.cmake
    # 8.0.16+
    depends_on('boost@1.69.0 cxxstd=98', type='build', when='@8.0.16: cxxstd=98')
    depends_on('boost@1.69.0 cxxstd=11', type='build', when='@8.0.16: cxxstd=11')
    depends_on('boost@1.69.0 cxxstd=14', type='build', when='@8.0.16: cxxstd=14')
    depends_on('boost@1.69.0 cxxstd=17', type='build', when='@8.0.16: cxxstd=17')
    # 8.0.14--8.0.15
    depends_on('boost@1.68.0 cxxstd=98', type='build', when='@8.0.14:8.0.15 cxxstd=98')
    depends_on('boost@1.68.0 cxxstd=11', type='build', when='@8.0.14:8.0.15 cxxstd=11')
    depends_on('boost@1.68.0 cxxstd=14', type='build', when='@8.0.14:8.0.15 cxxstd=14')
    depends_on('boost@1.68.0 cxxstd=17', type='build', when='@8.0.14:8.0.15 cxxstd=17')
    # 8.0.12--8.0.13
    depends_on('boost@1.67.0 cxxstd=98', type='build', when='@8.0.12:8.0.13 cxxstd=98')
    depends_on('boost@1.67.0 cxxstd=11', type='build', when='@8.0.12:8.0.13 cxxstd=11')
    depends_on('boost@1.67.0 cxxstd=14', type='build', when='@8.0.12:8.0.13 cxxstd=14')
    depends_on('boost@1.67.0 cxxstd=17', type='build', when='@8.0.12:8.0.13 cxxstd=17')
    # 8.0.11
    depends_on('boost@1.66.0 cxxstd=98', type='build', when='@8.0.11 cxxstd=98')
    depends_on('boost@1.66.0 cxxstd=11', type='build', when='@8.0.11 cxxstd=11')
    depends_on('boost@1.66.0 cxxstd=14', type='build', when='@8.0.11 cxxstd=14')
    depends_on('boost@1.66.0 cxxstd=17', type='build', when='@8.0.11 cxxstd=17')
    # 5.7.X
    depends_on('boost@1.59.0 cxxstd=98', when='@5.7.0:5.7.999 cxxstd=98')
    depends_on('boost@1.59.0 cxxstd=11', when='@5.7.0:5.7.999 cxxstd=11')
    depends_on('boost@1.59.0 cxxstd=14', when='@5.7.0:5.7.999 cxxstd=14')
    depends_on('boost@1.59.0 cxxstd=17', when='@5.7.0:5.7.999 cxxstd=17')

    depends_on('ncurses')
    depends_on('openssl')
    depends_on('perl', type=['build', 'test'], when='@:7.99.99')
    depends_on('bison@2.1:', type='build', when='@develop')
    depends_on('m4', type='build', when='@develop platform=solaris')

    patch('fix-no-server-5.5.patch', level=1, when='@5.5.0:5.5.999')

    def url_for_version(self, version):
        url = "https://dev.mysql.com/get/Downloads/MySQL-{0}/mysql-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def cmake_args(self):
        spec = self.spec
        options = []
        if 'boost' in spec:
            options.append('-DBOOST_ROOT={0}'.format(spec['boost'].prefix))
        if '+client_only' in self.spec:
            options.append('-DWITHOUT_SERVER:BOOL=ON')
        return options

    def _fix_dtrace_shebang(self, spack_env):
        # dtrace may cause build to fail because it uses
        # '/usr/bin/python' in the shebang. To work around that we copy
        # the original script into a temporary folder, and change the
        # shebang to '/usr/bin/env python'. Treatment adapted from that
        # used in glib recipe per M. Culpo @b2822b258.
        dtrace = which('dtrace').path
        dtrace_copy_path = os.path.join(tempfile.mkdtemp(), 'dtrace-copy')
        dtrace_copy = os.path.join(dtrace_copy_path, 'dtrace')
        mkdirp(dtrace_copy_path)
        copy(dtrace, dtrace_copy)
        filter_file(
            '^#!/usr/bin/python',
            '#!/usr/bin/env python',
            dtrace_copy
        )
        # To have our own copy of dtrace in PATH, we need to
        # prepend to PATH the temporary folder where it resides.
        spack_env.prepend_path('PATH', dtrace_copy_path)

    @run_before('cmake')
    def _maybe_fix_dtrace_shebang(self):
        if 'python' in self.spec.flat_dependencies() and \
           self.spec.satisfies('@:7.99.99'):
            self._fix_dtrace_shebang(spack_env)

    def setup_environment(self, spack_env, run_env):
        cxxstd = self.spec.variants['cxxstd'].value
        flag = getattr(self.compiler, 'cxx{0}_flag'.format(cxxstd))
        if flag:
            spack_env.append_flags('CXXFLAGS', flag)
        if cxxstd != '98':
            if int(cxxstd) > 11:
                spack_env.append_flags('CXXFLAGS',
                                       '-Wno-deprecated-declarations')
            if int(cxxstd) > 14:
                spack_env.append_flags('CXXFLAGS', '-Wno-error=register')
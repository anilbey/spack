# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class Mvapich2(AutotoolsPackage):
    """MVAPICH2 is an MPI implementation for Infiniband networks."""
    homepage = "http://mvapich.cse.ohio-state.edu/"
    url = "http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.2.tar.gz"
    list_url = "http://mvapich.cse.ohio-state.edu/downloads/"

    # Prefer the latest stable release
    version('2.3.4', sha256='7226a45c7c98333c8e5d2888119cce186199b430c13b7b1dca1769909e68ea7a', preferred=True)
    version('2.3.3', sha256='41d3261be57e5bc8aabf4e32981543c015c5443ff032a26f18205985e18c2b73')
    version('2.3.2', sha256='30cc0d7bcaa075d204692f76bca4d65a539e0f661c7460ffa9f835d6249e1ebf')
    version('2.3.1', sha256='314e12829f75f3ed83cd4779a972572d1787aac6543a3d024ea7c6080e0ee3bf')
    version('2.3', sha256='01d5fb592454ddd9ecc17e91c8983b6aea0e7559aa38f410b111c8ef385b50dd')
    version('2.3rc2', sha256='dc3801f879a54358d17002a56afd45186e2e83edc5b8367b5c317e282eb6d6bf')
    version('2.3rc1', sha256='607d309c864a6d57f5fa78fe6dd02368919736b8be0f4ddb938aba303ef9c45c')
    version('2.3a', sha256='7f0bc94265de9f66af567a263b1be6ef01755f7f6aedd25303d640cc4d8b1cff')
    version('2.2', sha256='791a6fc2b23de63b430b3e598bf05b1b25b82ba8bf7e0622fc81ba593b3bb131')
    version('2.1', sha256='49f3225ad17d2f3b6b127236a0abdc979ca8a3efb8d47ab4b6cd4f5252d05d29')

    provides('mpi')
    provides('mpi@:3.0')

    variant('debug', default=False,
            description='Enable debug info and error messages at run-time')

    variant('cuda', default=False,
            description='Enable CUDA extension')

    variant('regcache', default=True,
            description='Enable memory registration cache')

    # Accepted values are:
    #   single      - No threads (MPI_THREAD_SINGLE)
    #   funneled    - Only the main thread calls MPI (MPI_THREAD_FUNNELED)
    #   serialized  - User serializes calls to MPI (MPI_THREAD_SERIALIZED)
    #   multiple    - Fully multi-threaded (MPI_THREAD_MULTIPLE)
    #   runtime     - Alias to "multiple"
    variant(
        'threads',
        default='multiple',
        values=('single', 'funneled', 'serialized', 'multiple'),
        multi=False,
        description='Control the level of thread support'
    )

    # 32 is needed when job size exceeds 32768 cores
    variant(
        'ch3_rank_bits',
        default='32',
        values=('16', '32'),
        multi=False,
        description='Number of bits allocated to the rank field (16 or 32)'
    )

    variant(
        'process_managers',
        description='List of the process managers to activate',
        values=disjoint_sets(
            ('auto',), ('slurm',), ('hydra', 'gforker', 'remshell')
        ).prohibit_empty_set().with_error(
            "'slurm' or 'auto' cannot be activated along with "
            "other process managers"
        ).with_default('auto').with_non_feature_values('auto'),
    )

    variant(
        'fabrics',
        description='The fabric enabled for this build',
        default='psm',
        values=(
            'psm', 'psm2', 'sock', 'nemesisib', 'nemesis', 'mrail',
            'nemesisibtcp', 'nemesistcpib', 'nemesisofi'
        )
    )

    variant(
        'alloca',
        default=False,
        description='Use alloca to allocate temporary memory if available'
    )

    variant(
        'file_systems',
        description='List of the ROMIO file systems to activate',
        values=auto_or_any_combination_of(
            'ime', 'lustre', 'gpfs', 'nfs', 'ufs'
        ),
    )

    depends_on('findutils', type='build')
    depends_on('bison', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('zlib')
    depends_on('libpciaccess', when=(sys.platform != 'darwin'))
    depends_on('libxml2')
    depends_on('cuda', when='+cuda')
    depends_on('psm', when='fabrics=psm')
    depends_on('opa-psm2', when='fabrics=psm2')
    depends_on('rdma-core', when='fabrics=mrail')
    depends_on('rdma-core', when='fabrics=nemesisib')
    depends_on('rdma-core', when='fabrics=nemesistcpib')
    depends_on('rdma-core', when='fabrics=nemesisibtcp')
    depends_on('libfabric', when='fabrics=nemesisofi')
    depends_on('slurm', when='process_managers=slurm')

    conflicts('fabrics=psm2', when='@:2.1')  # psm2 support was added at version 2.2

    filter_compiler_wrappers(
        'mpicc', 'mpicxx', 'mpif77', 'mpif90', 'mpifort', relative_root='bin'
    )

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpicxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    @property
    def process_manager_options(self):
        spec = self.spec

        other_pms = []
        for x in ('hydra', 'gforker', 'remshell'):
            if 'process_managers={0}'.format(x) in spec:
                other_pms.append(x)

        opts = []
        if len(other_pms) > 0:
            opts = ['--with-pm=%s' % ':'.join(other_pms)]

        # See: http://slurm.schedmd.com/mpi_guide.html#mvapich2
        if 'process_managers=slurm' in spec:
            opts = [
                '--with-pmi=pmi2',
                '--with-pm=slurm',
                '--with-slurm={0}'.format(spec['slurm'].prefix),
            ]

        return opts

    @property
    def network_options(self):
        opts = []
        # From here on I can suppose that only one variant has been selected
        if 'fabrics=psm' in self.spec:
            opts = [
                "--with-device=ch3:psm",
                "--with-psm={0}".format(self.spec['psm'].prefix)
            ]
        elif 'fabrics=psm2' in self.spec:
            opts = [
                "--with-device=ch3:psm",
                "--with-psm2={0}".format(self.spec['opa-psm2'].prefix)
            ]
        elif 'fabrics=sock' in self.spec:
            opts = ["--with-device=ch3:sock"]
        elif 'fabrics=nemesistcpib' in self.spec:
            opts = ["--with-device=ch3:nemesis:tcp,ib"]
        elif 'fabrics=nemesisibtcp' in self.spec:
            opts = ["--with-device=ch3:nemesis:ib,tcp"]
        elif 'fabrics=nemesisib' in self.spec:
            opts = ["--with-device=ch3:nemesis:ib"]
        elif 'fabrics=nemesis' in self.spec:
            opts = ["--with-device=ch3:nemesis"]
        elif 'fabrics=mrail' in self.spec:
            opts = ["--with-device=ch3:mrail", "--with-rdma=gen2",
                    "--disable-mcast"]
        elif 'fabrics=nemesisofi' in self.spec:
            opts = ["--with-device=ch3:nemesis:ofi",
                    "--with-ofi={0}".format(self.spec['libfabric'].prefix)]
        return opts

    @property
    def file_system_options(self):
        spec = self.spec
        opts = []

        fs = []
        for x in ('ime', 'lustre', 'gpfs', 'nfs', 'ufs'):
            if 'file_systems={0}'.format(x) in spec:
                fs.append(x)
                # TODO : when IME package will be added, replace these paths
                if x == 'ime':
                    opts = ["CFLAGS=-I/opt/ddn/ime/include",
                            "LDFLAGS=-L/opt/ddn/ime/lib",
                            "LIBS=-lim_client"]

        if len(fs) > 0:
            opts.append('--with-file-system=%s' % '+'.join(fs))

        return opts

    def setup_build_environment(self, env):
        # mvapich2 configure fails when F90 and F90FLAGS are set
        env.unset('F90')
        env.unset('F90FLAGS')

    def setup_run_environment(self, env):
        spec = self.spec
        if 'process_managers=slurm' in spec:
            env.set('SLURM_MPI_TYPE', 'pmi2')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        env.set('MPICXX', join_path(self.prefix.bin, 'mpicxx'))
        env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

        env.set('MPICH_CC', spack_cc)
        env.set('MPICH_CXX', spack_cxx)
        env.set('MPICH_F77', spack_f77)
        env.set('MPICH_F90', spack_fc)
        env.set('MPICH_FC', spack_fc)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc  = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
        self.spec.mpifc  = join_path(self.prefix.bin, 'mpif90')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')
        self.spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, 'libmpicxx.{0}'.format(dso_suffix)),
            join_path(self.prefix.lib, 'libmpi.{0}'.format(dso_suffix))
        ]

    @run_before('configure')
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError(
                'Mvapich2 requires both C and Fortran compilers!'
            )

    def configure_args(self):
        spec = self.spec
        args = [
            '--enable-shared',
            '--enable-romio',
            '--disable-silent-rules',
            '--disable-new-dtags',
            '--enable-fortran=all',
            "--enable-threads={0}".format(spec.variants['threads'].value),
            "--with-ch3-rank-bits={0}".format(
                spec.variants['ch3_rank_bits'].value),
        ]

        args.extend(self.enable_or_disable('alloca'))

        if '+debug' in self.spec:
            args.extend([
                '--disable-fast',
                '--enable-error-checking=runtime',
                '--enable-error-messages=all',
                # Permits debugging with TotalView
                '--enable-g=dbg',
                '--enable-debuginfo'
            ])
        else:
            args.append('--enable-fast=all')

        if '+cuda' in self.spec:
            args.extend([
                '--enable-cuda',
                '--with-cuda={0}'.format(spec['cuda'].prefix)
            ])
        else:
            args.append('--disable-cuda')

        if '+regcache' in self.spec:
            args.append('--enable-registration-cache')
        else:
            args.append('--disable-registration-cache')

        args.extend(self.process_manager_options)
        args.extend(self.network_options)
        args.extend(self.file_system_options)
        return args

##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel, \
    version_from_model_core_deps


class NeurodamusMousify(NeurodamusModel):
    """Neurodamus with built-in Mousify model
    """

    homepage = "ssh://bbpcode.epfl.ch/sim/models/mousify"
    git      = "ssh://bbpcode.epfl.ch/sim/models/mousify"

    mech_name = "mousify"

    # IMPORTANT: Register versions (only) here to make them stable
    # Final version name is combined e.g. "1.0-3.0.1"
    model_core_dep_v = (
        ('1.2', '3.1.0'),
        ('1.1', '3.0.2'),
    )
    version_from_model_core_deps(model_core_dep_v)

    version('develop', branch='master', submodules=True, get_full_repo=False)
    version('1.0', tag='1.0', submodules=True, get_full_repo=False)
    version('0.3', tag='0.3-1', submodules=True, get_full_repo=False)
    version('0.2', tag='0.2', submodules=True, get_full_repo=False)
    version('0.1', tag='0.1', submodules=True, get_full_repo=False)

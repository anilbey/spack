# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RStanheaders(RPackage):
    """The C++ header files of the Stan project are provided by this package,
    but it contains no R code, vignettes, or function documentation. There is a
    shared object containing part of the CVODES library, but it is not
    accessible from R. StanHeaders is only useful for developers who want to
    utilize the LinkingTo directive of their package's DESCRIPTION file to
    build on the Stan library without incurring unnecessary dependencies. The
    Stan project develops a probabilistic programming language that implements
    full or approximate Bayesian statistical inference via Markov Chain Monte
    Carlo or variational methods and implements (optionally penalized) maximum
    likelihood estimation via optimization. The Stan library includes an
    advanced automatic differentiation scheme, templated statistical and linear
    algebra functions that can handle the automatically differentiable scalar
    types (and doubles, ints, etc.), and a parser for the Stan language. The
    'rstan' package provides user-facing R functions to parse, compile, test,
    estimate, and analyze Stan models."""

    homepage = "http://mc-stan.org/"
    url      = "https://cloud.r-project.org/src/contrib/StanHeaders_2.10.0-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/StanHeaders"

    version('2.18.1-10', sha256='8a9f7e22105428e97d14f44f75395c37cf8c809de148d279c620024452b3565a')
    version('2.18.1', sha256='ce0d609a7cd11725b1203bdeae92acc54da3a48b8266eb9dbdb9d95b14df9209')
    version('2.17.1', sha256='4300a1910a2eb40d7a6ecabea3c1e26f0aa9421eeb3000689272a0f62cb80d97')
    version('2.10.0-2', sha256='ce4e335172bc65da874699302f6ba5466cdbcf69458c11954c0f131fc78b59b7')

    depends_on('r@3.4.0:', when='@2.18.0:', type=('build', 'run'))
    depends_on('pandoc', type='build')

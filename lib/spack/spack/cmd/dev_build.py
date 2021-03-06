# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os
import argparse

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.config
import spack.cmd
import spack.repo
import spack.cmd.common.arguments as arguments
from spack.stage import DIYStage

description = "developer build: build from code in current working directory"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['jobs', 'test', 'overwrite', 'yes_to_all'])
    subparser.add_argument(
        '-d', '--source-path', dest='source_path', default=None,
        help="path to source directory. defaults to the current directory")
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="don't try to install dependencies of requested packages")
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '--keep-prefix', action='store_true',
        help="do not remove the install prefix if installation fails")
    subparser.add_argument(
        '--skip-patch', action='store_true',
        help="skip patching for the developer build")
    subparser.add_argument(
        '-q', '--quiet', action='store_true', dest='quiet',
        help="do not display verbose build output while installing")
    subparser.add_argument(
        '-u', '--until', type=str, dest='until', default=None,
        help="phase to stop after when installing (default None)")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs to use for install. must contain package AND version")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])


def dev_build(self, args):
    if not args.spec:
        tty.die("spack dev-build requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    spec = specs[0]
    if not spack.repo.path.exists(spec.name):
        tty.die("No package for '{0}' was found.".format(spec.name),
                "  Use `spack create` to create a new package")

    tests = False
    if args.test == 'all':
        tests = True
    elif args.test == 'root':
        tests = [spec.name]

    if not spec.versions.concrete:
        tty.die(
            "spack dev-build spec must have a single, concrete version. "
            "Did you forget a package version number?")

    spec.concretize()
    package = spack.repo.get(spec)

    source_path = args.source_path
    if source_path is None:
        source_path = os.getcwd()
    source_path = os.path.abspath(source_path)

    # Forces the build to run out of the current directory.
    package.stage = DIYStage(source_path)

    # disable checksumming if requested
    if args.no_checksum or args.yes_to_all:
        spack.config.set('config:checksum', False, scope='command_line')

    kwargs = dict(
        make_jobs=args.jobs,
        keep_prefix=args.keep_prefix,
        install_deps=not args.ignore_deps,
        verbose=not args.quiet,
        keep_stage=True,   # don't remove source dir for DIY.
        tests=tests,
        dirty=args.dirty,
        stop_at=args.until)

    display_args = {
        'long': True,
        'show_flags': True,
        'variants': True
    }

    if package.installed:
        if args.overwrite:
            if not args.yes_to_all:
                tty.msg('The following package will be reinstalled:\n')

                t = spack.store.db.query(spec)
                spack.cmd.display_specs(t, **display_args)
                answer = tty.get_yes_or_no(
                    'Do you want to proceed?', default=False
                )
                if not answer:
                    tty.die('Reinstallation aborted.')
            with fs.replace_directory_transaction(spec.prefix):
                package.do_install(**kwargs)
        else:
            tty.error("Already installed in %s" % package.prefix)
            tty.msg("Uninstall or try adding a version suffix for this DIY build.")
            sys.exit(1)
            # Give the user a last chance to think about overwriting an already
            # existing installation
    else:
        if args.overwrite:
            tty.msg("The following spec will be freshly installed, "
                    "ignoring the --overwrite flag:")
            spack.cmd.display_specs([spec], **display_args)
        package.do_install(**kwargs)

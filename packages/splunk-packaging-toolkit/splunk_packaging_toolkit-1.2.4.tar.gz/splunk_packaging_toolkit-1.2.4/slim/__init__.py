# coding=utf-8
#
# Copyright © Splunk, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function, unicode_literals

from os.path import basename, splitext
from sys import argv

from . describe import describe
from . generate_manifest import generate_manifest
from . package import package
from . partition import partition
from . update_installation import update_installation
from . validate import validate

__build_number__ = '@SLIM_BUILD_NUMBER@'
__version__ = '1.2.0'


def _set_program_version():
    prog = splitext(basename(argv[0]))[0]
    return prog, prog + ' version ' + __version__ + '-' + __build_number__


program, version = _set_program_version()
del _set_program_version

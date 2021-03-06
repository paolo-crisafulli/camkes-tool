#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2017, Data61
# Commonwealth Scientific and Industrial Research Organisation (CSIRO)
# ABN 41 687 119 230.
#
# This software may be distributed and modified according to the terms of
# the BSD 2-Clause license. Note that NO WARRANTY is provided.
# See "LICENSE_BSD2.txt" for details.
#
# @TAG(DATA61_BSD)
#

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os, pylint, re, sys, unittest
from pylint import epylint

ME = os.path.abspath(__file__)

# Make CAmkES importable
sys.path.append(os.path.join(os.path.dirname(ME), '../../..'))

from camkes.internal.tests.utils import CAmkESTest

class TestPyLintOnSource(CAmkESTest):
    pass

def lint(self, path):
    stdout, stderr = epylint.py_run('%s --errors-only' % path, return_std=True)
    err = []
    for line in [x.strip() for x in stdout] + [x.strip() for x in stderr]:
        if line == 'No config file found, using default configuration':
            continue
        if line:
            err.append(line)
    if len(err) > 0:
        self.fail('\n'.join(err))

srcdir = os.path.join(os.path.dirname(ME), '..')
regex = re.compile(r'.*\.py$')
sub = re.compile(r'[^\w]')
for src in os.listdir(srcdir):
    if regex.match(src) is None:
        continue
    path = os.path.abspath(os.path.join(srcdir, src))
    name = 'test_%s' % sub.sub('_', src)
    setattr(TestPyLintOnSource, name, lambda self, path=path: lint(self, path))

if __name__ == '__main__':
    unittest.main()

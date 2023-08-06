# -*- coding: utf-8 -*-

##
# witness
#
#  Copyright 2017 by Matthieu Daumas <matthieu@daumas.me> and other authors.
#
# This file is a part of fuddly, as part of the knowledge component.
#
#  Licensed under GNU General Public License 3.0 or later.
#  Some rights reserved. See COPYING, AUTHORS.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>
##

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import operator
import sys

import witness as wit
import witness.oracle
import witness.source
import witness.fuzzy

assert sys.version_info >= (2, 7)


class naive(wit.oracle.backend):
    def __init__(self, parent):
        self.parent = parent
        self.source = wit.source.oracle_source(name='naive')
        self.size = 1
        self.reset()

    def reset(self, keep_history=False):
        new_history = wit.fuzzy.evidence(size=self.size, source=self.source)
        if keep_history:
            new_history.value[:len(self.history.value)] = self.history.value
        self.history = new_history
        self.history.static_source = True

    def submit(self, evidences):
        for e in evidences:
            if e.size > self.size:
                self.size = e.size
                self.reset(keep_history=True)
            wit.fuzzy.scale(self.history)
            self.history <<= e

    def query(self, evidences):
        output = []
        for e in evidences:
            assert e.size == self.size

            answer = e.clone()
            answer.merge_operator = operator.__and__

            answer <<= self.history

            answer.merge_operator = operator.add
            answer.source = self.source

            output.append(answer)
        return output

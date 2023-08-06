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

import sys

assert sys.version_info >= (2, 7)

# api version
api_version = (0, 0, 5)


# run tests
def test():
    import unittest

    suite = unittest.TestLoader().loadTestsFromName('witness.test_modules')
    unittest.TextTestRunner(verbosity=2).run(suite)


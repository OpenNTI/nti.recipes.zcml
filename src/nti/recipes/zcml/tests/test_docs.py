#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Doctest runner for 'nti.recipes.zcml'

Based on code originally licensed under the ZPL, Copyright (c) Zope
Corporation (tm) and Contributors. All rights reserved.

Modified by NextThought, 2013

$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

import os
import unittest
import doctest

import zc.buildout.tests
import zc.buildout.testing


from zope.testing import renormalizing

optionflags =  (doctest.ELLIPSIS |
				doctest.NORMALIZE_WHITESPACE |
				doctest.REPORT_ONLY_FIRST_FAILURE)
globs = {}
def setUp(test):
	zc.buildout.testing.buildoutSetUp(test)

	# Install the recipe in develop mode
	zc.buildout.testing.install_develop('nti.recipes.zcml', test)

	# Install any other recipes that should be available in the tests
#	zc.buildout.testing.install_develop('zc.recipe.deployment', test)
#	zc.buildout.testing.install_develop('manuel', test)
#	zc.buildout.testing.install_develop('zope.testing', test)
#	zc.buildout.testing.install_develop('six', test)
#	zc.buildout.testing.install_develop('zope.interface', test)
#	zc.buildout.testing.install_develop('zope.exceptions', test)

def test_suite():
	suite = unittest.TestSuite((
		doctest.DocFileSuite(
			'../../../../../README.rst',
			setUp=setUp,
			tearDown=zc.buildout.testing.buildoutTearDown,
			optionflags=optionflags,
			checker=renormalizing.RENormalizing([
				# If want to clean up the doctest output you
				# can register additional regexp normalizers
				# here. The format is a two-tuple with the RE
				# as the first item and the replacement as the
				# second item, e.g.
				# (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
				zc.buildout.testing.normalize_path,
				]),
			),
		))
	# Nose doesn't support suites.
	# quick hack to catch failures.
	result = suite.run( unittest.TestResult() )
	result.printErrors()
	if result.failures:
		val = ''
		for f in result.failures:
			for l in f:
				val += '\n%s' % l
		raise ValueError(val)
	return result

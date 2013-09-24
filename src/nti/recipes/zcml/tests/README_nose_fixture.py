#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fixture file for the doctests in README.rst.

$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


import zc.buildout.tests
import zc.buildout.testing



def setup_test(test):

	zc.buildout.testing.buildoutSetUp(test)

	# Install the recipe in develop mode
	zc.buildout.testing.install_develop('nti.recipes.zcml', test)

	# Install any other recipes that should be available in the tests
	#zc.buildout.testing.install('setuptools', test)
	#zc.buildout.testing.install('zc.buildout', test)
	import manuel
	import six
	import zope.testing
	import zope.interface
	import zope.exceptions
	import setuptools


	zc.buildout.testing.install('zc.recipe.deployment', test)
	zc.buildout.testing.install('manuel', test)
	zc.buildout.testing.install('zope.testing', test)
	zc.buildout.testing.install('six', test)
	zc.buildout.testing.install('zope.interface', test)
	zc.buildout.testing.install('zope.exceptions', test)

	# Having this set causes failures on OS X, at least.
	# It doesn't get abspath'd and the symlinks between
	# /var and /private/var seem to cause issues
	import os
	del os.environ['buildout-testing-index-url']


teardown_test = zc.buildout.testing.buildoutTearDown

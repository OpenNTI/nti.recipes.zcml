#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

import doctest
import unittest

import zc.buildout.tests
import zc.buildout.testing



def setUp(test):

    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('nti.recipes.zcml', test)

    # Install any other recipes that should be available in the tests
    #zc.buildout.testing.install('setuptools', test)
    #zc.buildout.testing.install('zc.buildout', test)
    # import manuel
    # import six
    # import zope.testing
    # import zope.interface
    # import zope.exceptions
    # import setuptools


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


tearDown = zc.buildout.testing.buildoutTearDown

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.rst',
            setUp=setUp, tearDown=tearDown),
    ))

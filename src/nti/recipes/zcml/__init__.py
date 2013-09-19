#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ZC.Buildout recipe for writing various ZCML include slugs.
Originally based on collective.recipe.zcml, but modified to not
be rigid about the type of ZCML file requested and the
paths to which they are written. Also requires the
use of zc.recipe.deployment.

$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import shutil
import re
#import zc.buildout

class ZCML(object):
	"""zc.buildout recipe"""

	def __init__(self, buildout, name, options):
		self.buildout, self.name, self.options = buildout, name, options
		if options['deployment']:
			options['etc'] = buildout[options['deployment']]['etc-directory']
		else:
			options['etc'] = options['etc-directory']

	def install(self):
		"""Installer"""
		created = self.build_package_includes()
		return tuple(created)

	update = install

	def build_package_includes(self):
		"""
		Create ZCML slugs.
		"""
		options = self.options
		etc = options['etc']
		package_match = re.compile(r'\w+([.]\w+)*$').match
		out = []

		for key in options:
			if not key.endswith('_zcml'):
				continue
			slug_name = key[:-5]
			slug_path = options[slug_name + '_location']
			slug_default_filename = options.get( slug_name + '_file', 'configure' )

			zcml = options[key]
			if not zcml:
				continue

			includes_path = os.path.join( etc, slug_path )
			if not os.path.exists(includes_path):
				os.mkdir(includes_path)

			zcml = zcml.split()
			if '*' in zcml:
				zcml.remove('*')
			else:
				shutil.rmtree(includes_path)
				os.mkdir(includes_path)

			n = 0
			for package in zcml:
				n += 1
				orig = package
				if ':' in package:
					package, filename = package.split(':')
				else:
					filename = None

				if '-' in package:
					package, suff = package.split('-')
				else:
					suff = slug_default_filename

				if filename is None:
					filename = suff + '.zcml'

				if not package_match(package):
					raise ValueError('Invalid zcml', orig)

				path = os.path.join(
					includes_path,
					"%3.3d-%s-%s.zcml" % (n, package, suff),
					)
				with open(path, 'w') as f:
					f.write(
						'<include package="%s" file="%s" />\n'
						% (package, filename) )
				out.append(path)
		return out

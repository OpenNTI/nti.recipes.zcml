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
import re
import zc.buildout
import errno

class ZCML(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        if 'deployment' in options:
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
            slug_features = options.get( slug_name + '_features', '' )
            slug_features = slug_features.split()

            zcml = options[key] or ''
            if not zcml and not slug_features:
                continue

            includes_path = os.path.join( etc, slug_path )
            if not os.path.exists(includes_path):
                try:
                    os.mkdir(includes_path)
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        raise zc.buildout.UserError("The parents of '%s' do not exist" % includes_path)
                    raise

            zcml = zcml.split()
            if '*' in zcml:
                zcml.remove('*')
            # We never need to remove the whole directory, buildout
            # will automatically uninstall any files we created in it
            # as needed

            if slug_features:
                features_zcml = ['\t<meta:provides feature="%s" />' % i
                                 for i in slug_features ]
                features_zcml.insert(0, '<configure xmlns="http://namespaces.zope.org/zope" xmlns:meta="http://namespaces.zope.org/meta">')
                features_zcml.append("</configure>")

                path = os.path.join( includes_path, '000-features.zcml' )
                with open(path, 'w') as f:
                    f.write( '\n'.join(features_zcml) )
                out.append(path)

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

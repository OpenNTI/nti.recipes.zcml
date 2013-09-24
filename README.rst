Supported options
=================

The recipe supports installing multiple different sets
of ZCML slugs in multiple different output directories.
These sets are specified in grouped options, where ``X``
is the common prefix shared by all options in the group.

X_zcml
	A list of zcml entires. Required.

	format::

		zcml := package ":" filename
		package := dottedname | dottedname "-" ( include_name )

	The ``filename`` is the fully specified file, such as
	``browser.zcml``, whereas the ``include_name`` is a relative
	portion mising the ``.zcml`` extension, defaulting to
	``configure`` (it was originally validated against a strict list
	of possibilities, but that is no longer the case). If the filename
	is not given, the ``include_name`` is used.

	If the zcml list contains the special key ``*``, then the
	directory containing the slugs is left in place and only specified
	entries are overwritten. Otherwise (by default), the entire
	directory is deleted and started from scratch.

X_location
	A directory name relative to the etc-directory
	to put the generated slugs in. Required.

X_file
	A convenient shortuct if all or most of the zcml entries would
	have the same ``include_name``. Set this option to make it the
	default instead of configure. Optional.

X_features
	If this optional directive is provided, it is a space-separated
	list of ZCML features that should be provided when the output
	directory is processed. These are provided in the first file.

There are two global options:

deployment
	The name of a ``zc.recipe.deployment`` part containing the
	directory definitions. We will use the ``etc-directory`` defined
	in this part as the base for locations.

etc-directory
	If you do not specify a ``deployment``, then this value will
	be used as the etc-directory.


Example usage
=============

We'll start by creating a buildout that uses the recipe::

	>>> write('buildout.cfg',
	... """
	... [buildout]
	... parts = test1
	...
	... [test1]
	... recipe = nti.recipes.zcml
	... etc-directory = ${buildout:directory}/zope/etc
	... package_location = package-includes
	... package_features = foo bar baz
	... package_zcml =
	...		my.package
	...		somefile:my.otherpackage
	...		my.thirdpackage-meta
	... """)

Running the buildout gives us::

	>>> print 'start', system(buildout) # doctest:+ELLIPSIS
	start Installing test1.
	While:
	  Installing test1.
	Error: The parents of '/.../sample-buildout/zope/etc/package-includes' do not exist

We need to have a valid etc directory. Let's create one::

	>>> mkdir("zope")
	>>> mkdir("zope", "etc")
	>>> print 'start', system(buildout) # doctest:+ELLIPSIS
	start Installing test1.

We now have a package include directory::

	>>> ls("zope", "etc")
	d  package-includes

It does contain ZCML slugs::

	>>> ls("zope", "etc", "package-includes")
	-  000-features.zcml
	-  001-my.package-configure.zcml
	-  002-somefile-configure.zcml
	-  003-my.thirdpackage-meta.zcml

These  files contain the usual stuff::

	>>> cat("zope", "etc", "package-includes", "000-features.zcml")
	<meta:provides feature="foo" />
	<meta:provides feature="bar" />
	<meta:provides feature="baz" />
	>>> cat("zope", "etc", "package-includes", "001-my.package-configure.zcml")
	<include package="my.package" file="configure.zcml" />
	>>> cat("zope", "etc", "package-includes", "002-somefile-configure.zcml")
	<include package="somefile" file="my.otherpackage" />
	>>> cat("zope", "etc", "package-includes", "003-my.thirdpackage-meta.zcml")
	<include package="my.thirdpackage" file="meta.zcml" />

That's all.

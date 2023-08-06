=======
Changes
=======

1.5 (2017-08-10)
================

- Remove dependency on ``Globals`` (Zope 4 forward compatibility).


1.4 (2016-10-24)
================

- Fix `moveObjectsByDelta()` to be usable with unicode ids.

- `getObjectPosition()` now raises a `LookupError` if object is not found.

- Move source code to new directory 'src'.

- Update `bootstrap.py`, so it accepts a pinned version of setuptools.

- Use `py.test` as the one and only testrunner.


1.3.0 (2011-03-15)
==================

- Updated package to use `Products.BTreeFolder2` >= 2.13.3, so most
  compatibility code added in version 1.2.1 could be removed, thus requiring
  at least `Products.BTreeFolder2` version 2.13.3.

- Removed not needed dependency on `Products.CMFCore`.


1.2.1 (2011-03-07)
==================

- Methods ``objectItems``, ``objectValues``, ``keys``, ``values`` and
  ``items`` returned values unordered when package was used together with
  `Products.BTreeFolder2` >= 2.13.


1.2.0 (2011-03-03)
==================

- Updated to run on Zope 2.12+, thus requiring at least this version.


1.1.0 (2009-04-01)
==================

- Initial packaging as an egg.

- Code cleanup.

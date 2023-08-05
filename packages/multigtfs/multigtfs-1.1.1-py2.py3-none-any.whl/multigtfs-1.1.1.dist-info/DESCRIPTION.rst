

**multigtfs** is an `Apache 2.0`_-licensed Django app that supports importing
and exporting of GTFS feeds.  All features of the `June 20, 2012 reference`_
are supported, including `all changes`_ up to February 17, 2014.
It allows multiple feeds to be stored in the database at once.

It requires a spatial databases compatible with GeoDjango_.  PostgreSQL_ 9.x
and PostGIS_ 2.x are recommended for development and production, since these
support all the GeoDjango features.

Status
======
multigtfs is ready for your GTFS project.

Point releases (such as 1.0.0 to 1.0.1) should be safe, only adding features or
fixing bugs.  Minor updates (1.0.1 to 1.1.0) may include significant changes
that will break relying code.  In the worst case scenario, you may need to
export your GTFS feeds in the original version, update multigtfs and your code,
and re-import.

multigtfs works with Django 1.8 (the long-term support, or LTS, release)
through 1.11.  Support will follow the Django supported releases, as well as
the Python versions supported by those releases.

All valid GTFS feeds are supported for import and export.  This includes
feeds with extra columns not yet included in the GTFS spec, and feeds that
omit ``calendar.txt`` in favor of ``calendar_dates.txt`` (such as the TriMet
archive feeds).  If you find a feed that doesn't work, `file a bug`_!

See the `issues list`_ for more details on bugs and feature requests.

Example project
===============
Check out the `example project`_.

If you have Docker_ installed and working, you can run the example project
without installing a database.

#. Add one or more feeds to import to the folder ``feeds/import``. You can find
   a feed for download at https://transitfeeds.com, such as
   `Tulsa Transit's Feed`_.
#. Initialize the containers with ``docker-compose up``.  After a few
   minutes, it will display::

    web_1  | Django version 1.8.18, using settings 'exploreproj.settings'
    web_1  | Development server is running at http://0.0.0.0:8000/
    web_1  | Using the Werkzeug debugger (http://werkzeug.pocoo.org/)
    web_1  | Quit the server with CONTROL-C.
    web_1  |  * Debugger is active!
    web_1  |  * Debugger PIN: XXX-XXX-XXX

#. Visit http://localhost:8000 to view the example project.

See the `example project`_ for more details.

Development
===========

:Code:           https://github.com/tulsawebdevs/django-multi-gtfs
:Issues:         https://github.com/tulsawebdevs/django-multi-gtfs/issues
:Dev Docs:       http://multigtfs.readthedocs.io/
:IRC:            irc://irc.freenode.net/tulsawebdevs


.. _`Apache 2.0`: http://choosealicense.com/licenses/apache/
.. _`June 20, 2012 reference`: https://developers.google.com/transit/gtfs/reference
.. _`all changes`: https://developers.google.com/transit/gtfs/guides/revision-history
.. _PostgreSQL: http://www.postgresql.org
.. _PostGIS: http://postgis.refractions.net
.. _GeoDjango: https://docs.djangoproject.com/en/dev/ref/contrib/gis/
.. _`file a bug`: https://github.com/tulsawebdevs/django-multi-gtfs/issues
.. _`issues list`: https://github.com/tulsawebdevs/django-multi-gtfs/issues?state=open
.. _`example project`: examples/explore/README.md
.. _`Docker`: https://www.docker.com
.. _`Tulsa Transit's Feed`: https://transitfeeds.com/p/tulsa-transit/521


Changelog
=========

1.1.1 (2017-08-02)
------------------
* Strip whitespace after commas in CSV files with skipinitialspace_
  (`issue #64`_, `PR #65`_ and `#68`_).
* Discard empty lines in CSV files (`issue #66`_, `PR #67`_)

.. _skipinitialspace: https://docs.python.org/2/library/csv.html#csv.Dialect.skipinitialspace
.. _`issue #64`: https://github.com/tulsawebdevs/django-multi-gtfs/issues/64
.. _`PR #65`: https://github.com/tulsawebdevs/django-multi-gtfs/pull/65
.. _`#68`: https://github.com/tulsawebdevs/django-multi-gtfs/pull/68
.. _`issue #66`: https://github.com/tulsawebdevs/django-multi-gtfs/issues/66
.. _`PR #67`: https://github.com/tulsawebdevs/django-multi-gtfs/pull/67

1.1.0 (2017-07-09)
------------------
* Add support for Django 1.10 and 1.11
* Drop support for Django 1.7 and earlier, and for South migrations. If you
  are using these, upgrade to 1.0.0 first, migrate your codebase to Django 1.8
  and Django migrations, then update to 1.1.0.
* Move Python 2 / Python 3 and other compatibilty code to
  ``multigtfs/compat.py``.  Exclude this file from the ``make qa`` coverage
  report, unless the ``COVERAGE_COMPAT`` environment variable is set.  Because
  the cross-environment code is now in this file, many lines will be uncovered
  in a particular environment, while other files should be 100% covered. This
  file is tested in the supported environments in TravisCI, and a combined
  coverage report is generated in Coveralls, where ``compat.py`` should be 100%
  covered.
* Add a dockerized environment for the explore example app, and run it under
  Django 1.11.
* Whitespace-only values in import files are treated as empty values
  (`PR #56`_)

.. _`PR #56`: https://github.com/tulsawebdevs/django-multi-gtfs/pull/56

1.0.0 (2016-03-29)
------------------
* The project has been production-ready for a while. Updating the version
  number and the PyPI classifiers to reflect that.
* Add support for Django 1.7 through 1.9, and a compatibility layer to handle
  future versions.
* Add support for transitioning from South to Django migrations.



Older changes can be found in the `full documention`_.

.. _`full documention`: http://multigtfs.readthedocs.io/en/latest/changelog.html



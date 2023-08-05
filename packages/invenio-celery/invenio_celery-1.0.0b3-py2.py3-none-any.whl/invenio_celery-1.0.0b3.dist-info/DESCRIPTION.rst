..
    This file is part of Invenio.
    Copyright (C) 2015, 2017 CERN.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.

================
 Invenio-Celery
================

.. image:: https://img.shields.io/travis/inveniosoftware/invenio-celery.svg
        :target: https://travis-ci.org/inveniosoftware/invenio-celery

.. image:: https://img.shields.io/coveralls/inveniosoftware/invenio-celery.svg
        :target: https://coveralls.io/r/inveniosoftware/invenio-celery

.. image:: https://img.shields.io/github/tag/inveniosoftware/invenio-celery.svg
        :target: https://github.com/inveniosoftware/invenio-celery/releases

.. image:: https://img.shields.io/pypi/dm/invenio-celery.svg
        :target: https://pypi.python.org/pypi/invenio-celery

.. image:: https://img.shields.io/github/license/inveniosoftware/invenio-celery.svg
        :target: https://github.com/inveniosoftware/invenio-celery/blob/master/LICENSE


Celery distributed task queue module for Invenio.

Invenio-Celery is a small discovery layer that takes care of discovering and
loading tasks from other Invenio modules, as well as providing configuration
defaults for Celery usage in Invenio. Invenio-Celery relies on Flask-CeleryExt
for integrating Flask and Celery with application factories.

Further documentation is available on https://invenio-celery.readthedocs.io/


..
    This file is part of Invenio.
    Copyright (C) 2015, 2016 CERN.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.


Changes
=======

Version 1.0.0b3 (released 2017-08-07)
-------------------------------------

- Refactoring for Invenio 3.

Version 0.1.1 (released 2015-10-02)
-----------------------------------

Improved features
~~~~~~~~~~~~~~~~~

- Disposes database connection when calling `close_database`.

Bug fixes
~~~~~~~~~

- Upgrades invenio-base minimum version to 0.3.0.
- Removes dependencies to invenio.testsuite and replaces them with
  invenio_testing.

Version 0.1.0 (released 2015-09-21)
-----------------------------------

- Initial public release.





.. image:: https://raw.githubusercontent.com/OneGov/onegov.notice/master/docs/onegov.notice.png
  :alt: States

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Notice follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Notice uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.notice.png
  :target: https://travis-ci.org/OneGov/onegov.notice
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.notice/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.notice?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://img.shields.io/pypi/v/onegov.notice.svg
  :target: https://pypi.python.org/pypi/onegov.notice
  :alt: Latest PyPI Release

License
-------
onegov.notice is released under GPLv2

Changelog
---------
0.0.2 (2017-08-09)
~~~~~~~~~~~~~~~~~~~

- Allows to filter notices by a search term.
  [msom]

- Allows to filter notices by user IDs.
  [msom]

0.0.1 (2017-07-14)
~~~~~~~~~~~~~~~~~~

- Initial Release



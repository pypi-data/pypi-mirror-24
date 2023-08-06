

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Install jest and run it::

    npm install
    npm t

Conventions
-----------

Onegov Gazette follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Gazette uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.gazette.png?branch=master
  :target: https://travis-ci.org/OneGov/onegov.gazette
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.gazette/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.gazette?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://img.shields.io/pypi/v/onegov.gazette.svg
  :target: https://pypi.python.org/pypi/onegov.gazette
  :alt: Latest PyPI Release

License
-------
onegov.gazette is released under GPLv2

Changelog
---------
0.1.1 (2017-08-21)
~~~~~~~~~~~~~~~~~~~

- Fixes ordering by first issue.
  [msom]

0.1.0 (2017-08-21)
~~~~~~~~~~~~~~~~~~~

- Shows the name of the logged-in user.
  [msom]

- Reduces the font size of the title in the preview.
  [msom]

- Omits the emails on publishing.
  [msom]

- Sends an email when creating a user.
  [msom]

- Adds statistics to the menu.
  [msom]

- Adds a state filter to the statistics.
  [msom]

- Shows the weekday in the add/edit notice form.
  [msom]

- Adds comments for rejecting notices.
  [msom]

- Sanitizes HTML much stricter.
  [msom]

- Allows to delete users with official notices.
  [msom]

- Allows to filter notices by a search term.
  [msom]

- Allows admins to delete submitted and published notices.
  [msom]

- Adds organizations to notices.
  [msom]

- Removes hierarchy from categories.
  [msom]

- Allows to order notices.
  [msom]

- Adds filters for organizations and categories to the edit/create notice views.
  [msom]

- Allows to show the later issues in the edit/create notice views, too.
  [msom]

- Adds deadlines to issues.
  [msom]

- Adds date filters to statistices.
  [msom]

- Adds an accepted state.
  [msom]

- Caches the user and group name on notices in case they get deleted.
  [msom]

- Caches the user name on notice changes in case they get deleted.
  [msom]

- Shows notices for the same group.
  [msom]

0.0.4 (2017-08-03)
~~~~~~~~~~~~~~~~~~~

- Switches from onegov.testing to onegov_testing.
  [href]

0.0.3 (2017-07-17)
~~~~~~~~~~~~~~~~~~~

- Add github deploy key.
  [msom]

0.0.2 (2017-07-17)
~~~~~~~~~~~~~~~~~~~

- Sends emails on publish/reject.
  [msom]

- Adds a copy option.
  [msom]

- Adds statistics views.
  [msom]

- Adds a preview view.
  [msom]

0.0.1 (unreleased)
~~~~~~~~~~~~~~~~~~

- Initial Release.
  [msom]



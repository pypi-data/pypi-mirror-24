.. _dev_guidelines:

Development Guidelines for stestr
=================================

Coding style
------------

PEP-8 is used for changes. We enforce running flake8 prior to landing any
commits.

Testing and QA
--------------

For stestr please add tests where possible. There is no requirement
for one test per change (because somethings are much harder to automatically
test than the benefit from such tests). But, if unit testing is reasonable it
will be expected to be present before it can merge.

Running the tests
-----------------

Generally just ``tox`` is all that is needed to run all the tests. However
if dropping into pdb, it is currently more convenient to use
``python -m testtools.run testrepository.tests.test_suite``.


Releasing
---------

Add release notes using `reno`_ prior to pushing the release to pypi. Versioning
is handled automatically by pbr, just make sure the tag is a valid version
number. The repo uses semver to dictate version number increments.

.. _reno: http://docs.openstack.org/developer/reno/

Release Notes
'''''''''''''
When making changes to any user facing interface we need to be sure to add a
release note documenting the change for the next release. This includes any
changes to a stable python interfaces that we support externally (including
adding an API), the CLI, deprecation of a feature, etc.

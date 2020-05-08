=========
Changelog
=========

..
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.
    To add a new change log entry, please see
    https://docs.pulpproject.org/contributing/git.html#changelog-update

    WARNING: Don't drop the next directive!

.. towncrier release notes start

3.3.1 (2020-05-08)
==================


Features
--------

- Introduced a CentOS version check
  `#6102 <https://pulp.plan.io/issues/6102>`_
- Replaced nginx/apache alias with proxying to whitenoise
  `#6561 <https://pulp.plan.io/issues/6561>`_
- Created a directory for Pulp nginx snippets
  `#6594 <https://pulp.plan.io/issues/6594>`_


Bugfixes
--------

- Fixed: pulp_installer devel role failing on CentOS 8 Stream (pre-8.2) with a module metadata error for the dependency criu.
  `#6509 <https://pulp.plan.io/issues/6509>`_
- Fixed several issues that cause the pre-flight check to not enforce (not terminating the install early on), which would lead to the instaler erroring at collectstatic, and leave users with a broken pulp installation.
  `#6623 <https://pulp.plan.io/issues/6623>`_
- Fixed the pulpcore/plugin compatibility check not enforcing on upgrades from Pulp prior to 3.2.0, potentially resulting in a failure on collectstatic.
  `#6642 <https://pulp.plan.io/issues/6642>`_
- Fixed the pulpcore/plugin compatibility check accidentally enforcing on upgrades when plugins have their upgrade variable specified, and the latest version of the plugin actually is compatible.
  `#6643 <https://pulp.plan.io/issues/6643>`_
- Fixed the pulpcore/plugin compatibility check not enforcing on upgrades when some currently installed plugins are not specified by the user in pulp_install_plugins.
  `#6644 <https://pulp.plan.io/issues/6644>`_
- Fixed the pulpcore/plugin compatibility check getting not enforcing when it needs the prereq roles applied to evaluate compatibility. It now runs before (and if necessary, after) the prereq roles.
  `#6645 <https://pulp.plan.io/issues/6645>`_
- Fixed pre-flight check producing an error (and accidentally enforcing) when a package is installed system-wide at a version that is not available on PyPI. This issue was never present on the previous release, only on the develoment branch.
  `#6689 <https://pulp.plan.io/issues/6689>`_
- Fixed pre-flight check producing an error (and accidentally enforcing) when trying & failing to build certain packages from PyPI that are actually available as a system-wide (RPM/deb-installed) package in the virtualenv. This issue was never present on the previous release, only on the develoment branch.
  `#6690 <https://pulp.plan.io/issues/6690>`_


Deprecations and Removals
-------------------------

- Removed the pulp_webserver_static_dir option.
  This fixes a bug where installations served content they should not.
  `#6601 <https://pulp.plan.io/issues/6601>`_


Misc
----

- `#6508 <https://pulp.plan.io/issues/6508>`_, `#6535 <https://pulp.plan.io/issues/6535>`_, `#6587 <https://pulp.plan.io/issues/6587>`_, `#6602 <https://pulp.plan.io/issues/6602>`_, `#6666 <https://pulp.plan.io/issues/6666>`_


----

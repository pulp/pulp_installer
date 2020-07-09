Changelog
=========

<!---
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.
    To add a new change log entry, please see
    https://docs.pulpproject.org/contributing/git.html#changelog-update

    WARNING: Don't drop the next directive!
--->

<!-- TOWNCRIER -->

3.5.0 (2020-07-09)
==================


Breaking Change
---------------
- New list of Ansible roles to run - [blog post](https://pulpproject.org/2020/07/09/pulp-3.5-installer-roles/)


Features
--------

- Add the ability to install Pulp from Linux distro (RPM) packages.
  [#6793](https://pulp.plan.io/issues/6793)
- Let users specify an RPM repo containing Pulp. Introduces the new variable: `pulp_pkg_repo`
  [#6794](https://pulp.plan.io/issues/6794)
- Add variables so users can specify the names of each RPM package to install (pulp_pkg_pulpcore_name
  & pulp_install_plugins's pkg_name) or to just override the prefix (pulp_pkg_name_prefix).
  [#6795](https://pulp.plan.io/issues/6795)
- Merging the pulp_rpm_prerequisites role into pulp_installer
  [#6799](https://pulp.plan.io/issues/6799)
- Allow user to specify redis package and service name.
  [#6895](https://pulp.plan.io/issues/6895)
- Allow one to specify a `pulp_ld_library_path` when wanted
  [#6913](https://pulp.plan.io/issues/6913)
- Unify the use of `pulp_content_bind` and `pulp_api_bind` across all network facing role. this
  inherently allow one to rely on Unix Domain Socket (UDS) if wanted based on the deployment
  scenario.
  [#6921](https://pulp.plan.io/issues/6921)
- Allow Nginx to listen for both IPv4 and IPv6 connections.
  [#6923](https://pulp.plan.io/issues/6923)
- Allow a user to use Unix Domain Socket (UDS) for the redis server.
  [#6931](https://pulp.plan.io/issues/6931)
- Set httpd_can_network_connect SELinux boolean when needed.
  [#6998](https://pulp.plan.io/issues/6998)
- Provide a single "pulp_all_services" role that users can specify instead of the current role list,
  and refactor the underlying roles and their dependency tree.
  [#7005](https://pulp.plan.io/issues/7005)
- Split the pulp_database role into pulp_database (installs postgres database)
  and pulp_database_config (configures Pulp database) for the sake of proper
  design. pulp_database no longer depends on pulp_common, so it can now be run
  against a separate database server without Pulp installed.
  [#7037](https://pulp.plan.io/issues/7037)
- Provide the "pulp_services" role that users can specify to install all of Pulp's first-party
  services, but not its third-party services (database server, redis server & webserver.)
  [#7038](https://pulp.plan.io/issues/7038)


Bugfixes
--------

- Fix webserver snippets not being installed when pulp_install_dir is changed from the default value.
  [#6956](https://pulp.plan.io/issues/6956)
- Fix documentation about certain variables being required, and error early with clear error messages
  if they are unset or set to empty strings.
  [#6958](https://pulp.plan.io/issues/6958)
- Add new RHUI repo name `rhel-7-server-rhui-optional-rpms` in `rhel7_optional_repo`.
  [#6960](https://pulp.plan.io/issues/6960)
- Fix apache installation
  [#7010](https://pulp.plan.io/issues/7010)
- Fix issue whereby for certain users, the firewall may not be configured.
  Also fix an issue whereby for certain pulp_devel role users, the Galaxy NG WebUI may not be built.
  [#7062](https://pulp.plan.io/issues/7062)


Improved Documentation
----------------------

- Adding changelog to readthedocs site
  [#7033](https://pulp.plan.io/issues/7033)
- Removing outdated reference to unavailablity of Roles on Ansible Galaxy.
  [#7055](https://pulp.plan.io/issues/7055)


Deprecations and Removals
-------------------------

- The `pulp_api_host` (127.0.0.1) and `pulp_api_port` (24817) have been removed and replaced by
  `pulp_api_bind` (127.0.0.1:24817). Same happened for `pulp_content_host` and `pulp_content_port`
  in favor of `pulp_content_bind`.
  [#6921](https://pulp.plan.io/issues/6921)
- Removed `pulp_redis` dependency from `pulp_workers` and `pulp_resource_manager`.
  Users need to adjust their playbook to run the `pulp_redis` role.
  [#6975](https://pulp.plan.io/issues/6975)
- `pulp_database`, which is now separate from `pulp_database_config`, no longer
  understands the variable `pulp_install_db`. Installing the postgres database
  server is now controlled by whether or not `pulp_database` is in the role list,
  and `pulp_database_config` must be in the list.
  [#7037](https://pulp.plan.io/issues/7037)
- Removed the task to add a redis PPA on all Ubuntu releases.
  Existing Ubuntu Pulp installations will still have the PPA enabled.
  [#7063](https://pulp.plan.io/issues/7063)


Misc
----

- [#6796](https://pulp.plan.io/issues/6796), [#6903](https://pulp.plan.io/issues/6903), [#6973](https://pulp.plan.io/issues/6973), [#7035](https://pulp.plan.io/issues/7035)


Devel
-----

- For developers, enable source-checkout of a plugin without also having a source checkout of pulpcore
  [#6910](https://pulp.plan.io/issues/6910)
- Adding dev type changelog
  [#7034](https://pulp.plan.io/issues/7034)


----


3.4.1 (2020-06-03)
==================


Bugfixes
--------

- Ensure that pip-tools is at least 5.2.0, so that the pre-flight (compatibility) check does not error on the attribute "editable".
  [#6864](https://pulp.plan.io/issues/6864)


Improved Documentation
----------------------

- Document how to install from galaxy
  [#6836](https://pulp.plan.io/issues/6836)
- Replaced root README.md with a short README.md pointing users to the docs site
  [#6843](https://pulp.plan.io/issues/6843)
- Added a contributing guide, and moved testing out of the home page to it.
  [#6862](https://pulp.plan.io/issues/6862)
- Added a documentation section on Recommended Versioning Workflows
  [#6874](https://pulp.plan.io/issues/6874)
- Document how to file an issue
  [#6879](https://pulp.plan.io/issues/6879)


----


3.4.0 (2020-05-27)
==================


Features
--------

- Make gunicorn --workers parameter configurable
  [#6727](https://pulp.plan.io/issues/6727)


Bugfixes
--------

- Enforce new lines when listing plugins on requirements.in
  [#6697](https://pulp.plan.io/issues/6697)
- Fixed CodeReady repo name for RHEL8 AWS installations
  [#6805](https://pulp.plan.io/issues/6805)


Improved Documentation
----------------------

- Document the conflict between `version` and `upgrade` when configuring plugins
  [#6669](https://pulp.plan.io/issues/6669)
- Documented system requirements for ansible when using the installer.
  [#6725](https://pulp.plan.io/issues/6725)


Deprecations and Removals
-------------------------

- Fitting directories into collection structure
  [#6458](https://pulp.plan.io/issues/6458)
- Renaming roles to use underscores rather than dashes
  [#6663](https://pulp.plan.io/issues/6663)
- Replaced `pulp_workers` dictionary variable with the `pulp_workers` integer variable.
  `pulp_workers` is now simply the number of workers.
  [#6774](https://pulp.plan.io/issues/6774)


----


3.3.1 (2020-05-08)
==================


Features
--------

- Introduced a CentOS version check
  [#6102](https://pulp.plan.io/issues/6102)
- Replaced nginx/apache alias with proxying to whitenoise
  [#6561](https://pulp.plan.io/issues/6561)
- Created a directory for Pulp nginx snippets
  [#6594](https://pulp.plan.io/issues/6594)


Bugfixes
--------

- Fixed: pulp_installer devel role failing on CentOS 8 Stream (pre-8.2) with a module metadata error for the dependency criu.
  [#6509](https://pulp.plan.io/issues/6509)
- Fixed several issues that cause the pre-flight check to not enforce (not terminating the install early on), which would lead to the instaler erroring at collectstatic, and leave users with a broken pulp installation.
  [#6623](https://pulp.plan.io/issues/6623)
- Fixed the pulpcore/plugin compatibility check not enforcing on upgrades from Pulp prior to 3.2.0, potentially resulting in a failure on collectstatic.
  [#6642](https://pulp.plan.io/issues/6642)
- Fixed the pulpcore/plugin compatibility check accidentally enforcing on upgrades when plugins have their upgrade variable specified, and the latest version of the plugin actually is compatible.
  [#6643](https://pulp.plan.io/issues/6643)
- Fixed the pulpcore/plugin compatibility check not enforcing on upgrades when some currently installed plugins are not specified by the user in pulp_install_plugins.
  [#6644](https://pulp.plan.io/issues/6644)
- Fixed the pulpcore/plugin compatibility check getting not enforcing when it needs the prereq roles applied to evaluate compatibility. It now runs before (and if necessary, after) the prereq roles.
  [#6645](https://pulp.plan.io/issues/6645)
- Fixed pre-flight check producing an error (and accidentally enforcing) when a package is installed system-wide at a version that is not available on PyPI. This issue was never present on the previous release, only on the develoment branch.
  [#6689](https://pulp.plan.io/issues/6689)
- Fixed pre-flight check producing an error (and accidentally enforcing) when trying & failing to build certain packages from PyPI that are actually available as a system-wide (RPM/deb-installed) package in the virtualenv. This issue was never present on the previous release, only on the develoment branch.
  [#6690](https://pulp.plan.io/issues/6690)


Deprecations and Removals
-------------------------

- Removed the pulp_webserver_static_dir option.
  This fixes a bug where installations served content they should not.
  [#6601](https://pulp.plan.io/issues/6601)


Misc
----

- [#6508](https://pulp.plan.io/issues/6508), [#6535](https://pulp.plan.io/issues/6535), [#6587](https://pulp.plan.io/issues/6587), [#6602](https://pulp.plan.io/issues/6602), [#6666](https://pulp.plan.io/issues/6666)


----

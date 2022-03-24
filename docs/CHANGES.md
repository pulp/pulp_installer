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

3.18.1 (2022-02-28)

Features
--------

- Optimize the role pulp_database for better performance.
  [#908](https://github.com/pulp/pulp_installer/issues/908)
- When in packages mode, install the package with the SELinux policies via an ansible task, rather than assuming it is a dependency (which is no longer the case.) The variable `pulp_pkg_selinux_name` was introduced to specify the name. Also introduce the variable `pulp_install_selinux_policies` to enable or disable installing the SELinux policies, regardless of whether in packages mode or pip mode.
  [#916](https://github.com/pulp/pulp_installer/issues/916)


Bugfixes
--------

- Fix being unable to install from katello's latest RPMs by no longer ignoring libcomps (reverts bugfix for #809)
  [#913](https://github.com/pulp/pulp_installer/issues/913)


----


3.18.0 (2022-02-22)

Features
--------

- The Pulp API can now be rerooted using the new ``API_ROOT`` setting. By default it is set to
  ``/pulp/``. Pulp appends the string ``api/v3/`` onto the value of ``API_ROOT``.
  [#892](https://github.com/pulp/pulp_installer/issues/892)


Bugfixes
--------

- Added `force_handlers: True` in every Playbook in order to flush handlers even if some tasks fail. Because we decided that this change will leave the system in a better more correct state if something went wrong.
  [#829](https://github.com/pulp/pulp_installer/issues/829)
- Removed extraneous use of become_user: root from devel role.
  [#844](https://github.com/pulp/pulp_installer/issues/844)
- Address failures on the task `pulp_common : Set state of pulpcore app` by having it do 5 retries over 60 seconds.
  [#868](https://github.com/pulp/pulp_installer/issues/868),
  [#886](https://github.com/pulp/pulp_installer/issues/886)
- Allow pulp to use pip>=22 again. This reverts the bugfix 'Fix pulp_installer failing on "pulp_common: Run pip-compile to check pulpcore/plugin compatibility" on most distros.' We can do this thanks to pip-tools 6.5.0 being released with pip 22 compatibility.
  [#876](https://github.com/pulp/pulp_installer/issues/876)
- Fix `pulp_webserver : Start and enable Apache` failing on CentOS Stream 8 container images (quay.io/centos/centos:stream8).
  [#878](https://github.com/pulp/pulp_installer/issues/878)


Misc
----

- [#382](https://github.com/pulp/pulp_installer/issues/382)


Devel
-----

- vagrant: Remove all EOL CentOS 8 (non-stream) boxes and environments, add centos8-stream-fips box and environments.
  [#881](https://github.com/pulp/pulp_installer/issues/881)
- Fixed unexpected download failures when we have the message `Failure downloading`.
  [#903](https://github.com/pulp/pulp_installer/issues/903)


----


3.17.2 (2022-02-02)
===================


Bugfixes
--------

- Fixed a problem in pulp_installer 3.17.0 that it would only install pulpcore 3.17.0 rather than the latest 3.17.z micro release. pulp_installer 3.17.0 users can work around by setting the variable `pulpcore_version: 3.17`
  [#862](https://github.com/pulp/pulp_installer/issues/862)


----


3.17.1 (2022-02-01)
===================


Features
--------

- Setting explicit permissions to files we modify or copy by installation process. Default is world readable (644 or 755).
  [#800](https://github.com/pulp/pulp_installer/issues/800)
- Set `pulp_pkg_repo` by default. Users can now install from packages merely by setting `pulp_install_source=packages`.
  [#816](https://github.com/pulp/pulp_installer/issues/816)
- Adds a `ptest` command to the pulp_devel role to run the functional tests for a specific project.
  [#848](https://github.com/pulp/pulp_installer/issues/848)
- Update SELinux policies to 1.2.7. Adds support for Pulp 3 connecting to remote repos through Squid and other web proxies.
  [#9450](https://github.com/pulp/pulp_installer/issues/9450)


Bugfixes
--------

- Fix building the collection failing on MacOS due to an `install` command error.
  [#823](https://github.com/pulp/pulp_installer/issues/823)
- Update pulpcore-selinux policies to 1.2.8. Fixes SELinux denials, and pulpcore-worker not starting when SELinux is enforcing, when using the new pulpcore tasking system.
  [#826](https://github.com/pulp/pulp_installer/issues/826)
- Workaround the geerlingguy.postgresql role failing to find the locale_gen module (and thus ansible runs failing) when using ansible-core.
  [#831](https://github.com/pulp/pulp_installer/issues/831)
- Fix pulp_installer failing to install rubygems on Debian 11 when using Ansible's main branch.
  [#833](https://github.com/pulp/pulp_installer/issues/833)
- Fix webservers symlinks
  [#834](https://github.com/pulp/pulp_installer/issues/834)
- Fix pulp_installer failing on "pulp_common: Run pip-compile to check pulpcore/plugin compatibility" on most distros. This occurs with pip 22.0 (just released) and pip-tools 6.4.0 (several months old and incompatible), so we are fixing it by limiting pip to 21 for now.
  [#858](https://github.com/pulp/pulp_installer/issues/858)
- Fixed a problem in pulp_installer 3.17.0 that it would only install pulpcore 3.17.0 rather than the latest 3.17.z micro release. pulp_installer 3.17.0 users can work around by setting the variable `pulpcore_version: 3.17`
  [#862](https://github.com/pulp/pulp_installer/issues/862)


Deprecations and Removals
-------------------------

- No longer support upgrading from packages prior to 3.6. Instead, users should download and run pulp_installer 3.14 with a 3.14 rpm repo, then upgrade to the current version.
  [#814](https://github.com/pulp/pulp_installer/issues/814)
- Ansible 2.9 and Python 2.7 are now further deprecated. We observed a bug whereby a pip_package_info task in the playbook fails after running the task `include_role: pulp_all_services`. The only fix for this bug is to upgrade to a known working and tested configuration like Python 3 and ansible-base 2.10+.
  [#836](https://github.com/pulp/pulp_installer/issues/836)
- CentOS 8 is now EOL, and thus Pulp no longer formally supports it. Pulp now only tests fresh installs with CentOS Stream 8, and with upgrades from CentOS 8 to CentOS Stream 8 (see migration instructions here https://centos.org/centos-stream/).
  [#860](https://github.com/pulp/pulp_installer/issues/860)


Devel
-----

- The installer is now tested against installing Pulp 3.16 RPM packages from theforeman.org .
  [#811](https://github.com/pulp/pulp_installer/issues/811)


----


3.17.0 (2021-12-14)

Features
--------

- Add Fedora 35 support
  [#799](https://github.com/pulp/pulp-operator/issues/799)
- Setting explicit permissions to files we modify or copy by installation process. Default is world readable (644 or 755).
  [#800](https://github.com/pulp/pulp-operator/issues/800)
- Update SELinux policies to 1.2.7. Adds support for Pulp 3 connecting to remote repos through Squid and other web proxies.
  [#9450](https://pulp.plan.io/issues/9450)


Bugfixes
--------

- Fix `pulp_common : Collect static content` sporadically failing when using a shared filesystem (.e.g, NFS) for `/var/lib/pulp` by running it sequentially across multiple Pulp nodes.
  [#790](https://github.com/pulp/pulp-operator/issues/790)
- Update packages mode support for Pulp 3.15 by changing the default package name prefix (`pulp_pkg_name_prefix`) from `python3-` to `tfm-pulpcore-python3-`.
  [#795](https://github.com/pulp/pulp-operator/issues/795)
- When installing from packages, fix pulpcore getting upgraded prematurely during "pulp_common : Install the Pulp undeclared yum package dependencies" by no longer installing pulpcore-selinux there. pulpcore-selinux will be installed as a declared dependency of pulpcore.
  [#798](https://github.com/pulp/pulp-operator/issues/798)
- Fixed pulp_installer failing when variables like `pulp_user_home` are set by specifying them in `/etc/pulp/settings.py`
  [#801](https://github.com/pulp/pulp-operator/issues/801)
- When installing in "packages" mode on EL7, workaround upgrading RPM packages by ignoring the latest libcomps. (Fixes error with upgrading python2-libcomps.)
  [#809](https://github.com/pulp/pulp-operator/issues/809)
- When installing in "packages" mode on EL8, fix upgrading from RPMs prior to 3.8 by excluding the no-longer-needed dependency python3-drf-yasg from upgrade.
  [#810](https://github.com/pulp/pulp-operator/issues/810)


Deprecations and Removals
-------------------------

- Removed the use_new_worker_type from dev-playbook example. And adjusted the resource-manager test
  in the health checks.
  [#9158](https://pulp.plan.io/issues/9158)


Devel
-----

- Added `pazurite` alias for enabling Azurite tests
  [#9499](https://pulp.plan.io/issues/9499)
- Fixed pulplift for installations with ansible 2.9
  [#9520](https://pulp.plan.io/issues/9520)


----


3.16.0 (2021-10-06)
===================


Features
--------

- Added support for specifying a minor version for `pulpcore_version`. A single version of pulp_installer can be used to
  install all bug fix releases within a minor release of pulpcore.
  [#8847](https://pulp.plan.io/issues/8847)
- Add SELinux support for the pulp-2to3-migration plugin by updating pulpcore-selinux (SELinux
  policies) to 1.2.6
  [#9468](https://pulp.plan.io/issues/9468)


Deprecations and Removals
-------------------------

- `pulp_version` variable has been replaced with `pulpcore_version`.
  [#8847](https://pulp.plan.io/issues/8847)
- Ensure resource manager is not started for pulpcore >= 3.16
  [#9386](https://pulp.plan.io/issues/9386)


Devel
-----

- Fix systemctl aliases from pulp_devel
  [#9460](https://pulp.plan.io/issues/9460)
- Set `client_max_body_size` to 10m for dev environments
  [#9463](https://pulp.plan.io/issues/9463)


----


3.15.2-2 (2021-09-22)
=====================


Features
--------

- Added a single systemd service to restart Pulp
  [#7006](https://pulp.plan.io/issues/7006)


----


3.15.2+1 (2021-09-10)
=====================


Misc
----

- [#9321](https://pulp.plan.io/issues/9321), [#9359](https://pulp.plan.io/issues/9359)


Devel
-----

- Run pulp_installer collection on pulplift
  [#9371](https://pulp.plan.io/issues/9371)


----


3.15.6 (2022-03-23)
===================

No significant changes.


----


3.15.5 (2022-03-15)
===================

No significant changes.


----


3.15.4-2 (2022-03-11)
=====================

Bugfixes
--------

- Update webserver symlink when needed
  [#939](https://pulp.plan.io/issues/939)


----


3.15.4-1 (2022-03-03)
=====================

Bugfixes
--------

- When in packages mode, install the package with the SELinux policies via an ansible task, rather than assuming it is a dependency (which is no longer the case.) The variable `pulp_pkg_selinux_name` was introduced to specify the name. Also introduce the variable `pulp_install_selinux_policies` to enable or disable installing the SELinux policies, regardless of whether in packages mode or pip mode.
  [#916](https://pulp.plan.io/issues/916)


----


3.15.4 (2022-03-03)
===================

No significant changes.


----


3.15.3-1 (2022-03-01)
=====================

Bugfixes
--------

- Removed extraneous use of become_user: root from devel role.
  [#844](https://pulp.plan.io/issues/844)


Deprecations and Removals
-------------------------

- CentOS 8 is now EOL, and thus Pulp no longer formally supports it. Pulp now only tests fresh installs with CentOS Stream 8, and with upgrades from CentOS 8 to CentOS Stream 8 (see migration instructions here https://centos.org/centos-stream/).
  [#860](https://pulp.plan.io/issues/860)


----


3.15.4 (2022-03-03)

No significant changes.


----


3.15.3-1 (2022-03-01)
=====================

Bugfixes
--------

- Removed extraneous use of become_user: root from devel role.
  [#844](https://pulp.plan.io/issues/844)


Deprecations and Removals
-------------------------

- CentOS 8 is now EOL, and thus Pulp no longer formally supports it. Pulp now only tests fresh installs with CentOS Stream 8, and with upgrades from CentOS 8 to CentOS Stream 8 (see migration instructions here https://centos.org/centos-stream/).
  [#860](https://pulp.plan.io/issues/860)


----


3.15.3 (2022-01-27)
===================

Bugfixes
--------

- Fix webservers symlinks
  [#834](https://github.com/pulp/pulp_installer/issues/834)


----


3.15.2 (2021-09-02)
===================


Misc
----

- [#9302](https://pulp.plan.io/issues/9302)


----


3.15.1 (2021-08-31)
===================


No significant changes.


----


3.15.0 (2021-08-26)
===================


Features
--------

- Added support for Python 3.8 as needed by pulpcore 3.15.
  [#9127](https://pulp.plan.io/issues/9127)
- Updated minimum supported version of Debian to 11 (Bullseye).
  Debian 10 does not provide Python 3.8+ which is needed for pulpcore 3.15 and Django 3.2.
  [#9136](https://pulp.plan.io/issues/9136)


Bugfixes
--------

- Generate DB fields encryption key before migrations
  [#9200](https://pulp.plan.io/issues/9200)
- Update pulpcore-selinux policies to 1.2.5. Adds support for Type=notify systemd Services (#9271). Hides a harmless SELinux denial from the audit logs when accessing /etc/httpd/mime.types on some systems like EL7 without `mailcap` installed.
  [#9272](https://pulp.plan.io/issues/9272)


Deprecations and Removals
-------------------------

- Removed support for Debian 10 due to lack of Python 3.8+ in that distribution.
  [#9136](https://pulp.plan.io/issues/9136)
- `pulp_db_fields_key_remote` is no longer available
  [#9200](https://pulp.plan.io/issues/9200)


----


3.14.10 (2022-01-07)

No significant changes.


----


3.14.9 (2022-01-07)

No significant changes.


----


3.14.8 (2021-10-14)
===================

No significant changes.


----


3.14.9 (2022-01-07)

No significant changes.


----


3.14.8 (2021-10-14)
===================

No significant changes.


----


3.14.8 (2021-10-14)
===================


No significant changes.


----


3.14.7-1 (2021-09-30)
=====================


Features
--------

- Add SELinux support for the pulp-2to3-migration plugin by updating pulpcore-selinux (SELinux
  policies) to 1.2.6
  [#9468](https://pulp.plan.io/issues/9468)


----


3.14.7 (2021-09-30)
===================


No significant changes.


----


3.14.6-1 (2021-09-09)
=====================


No significant changes.


----


3.14.6 (2021-09-02)
===================


No significant changes.


----


3.14.5 (2021-08-24)
===================

Features
--------

- Have systemd manage the pulpcore-api and pulpcore-content services as type=notify rather than type=simple. This means systemd will better understand whether the service is up and running before it lists it as "running".
  [#9271](https://pulp.plan.io/issues/9271)


----


3.14.4 (2021-08-12)
===================


Features
--------

- Add configuration needed for Galaxy api access log
  [#9177](https://pulp.plan.io/issues/9177)


----


3.14.3-1 (2021-08-04)
=====================


Bugfixes
--------

- Fix occasional failures on the tasks `pulp-webserver: Symlink Apache snippets` & `pulp-webserver: Symlink nginx snippets`.
  [#9139](https://pulp.plan.io/issues/9139)
- Fix the "markuppy" `pkg_resources.DistributionNotFound` error on the task
  `pulp_common : Collect static content`.
  This occurs when installing from RPM packages on EL8 (ever since EPEL8 released
  python-tablib-3.0.0-1.el8 on approximately 2021-07-23).
  [#9166](https://pulp.plan.io/issues/9166)


Devel
-----

- Ensure the requirements.in points to proper value fo the plugin when git_url
  is specified. Given this is run before the plugins is actually clone,
  source_dir repo is not yet available at that stage.
  [#9141](https://pulp.plan.io/issues/9141)


----


3.14.3 (2021-07-23)
===================


No significant changes.


----


3.14.2-1 (2021-07-21)
=====================


Bugfixes
--------

- Add ipv6 check for roles/pulp_webserver/templates/nginx.conf.j2 redirect rule using ansible facts
  [#9089](https://pulp.plan.io/issues/9089)
- Fixed the pre-flight check accidentally producing an error (and accidentally enforcing) on EL7 when not installing pulp-rpm. This bug was introduced in 3.11.0.
  [#9093](https://pulp.plan.io/issues/9093)
- Fixed the pre-flight check not being run when pulp-rpm is being installed, and `prereq_role` isn't explicitly specified.
  [#9095](https://pulp.plan.io/issues/9095)
- Fix pulp_database being incompatible with RHEL7 (since 3.11.0) by enabling the RHEL7 SCL repo on it. Introduces the new variable `rhel7_scl_repo`.
  [#9114](https://pulp.plan.io/issues/9114)


----


3.14.2 (2021-07-13)
===================


Bugfixes
--------

- Fix failure on task `pulp_api : Check for existing Pulp Database Encryption Key` when connecting to the ansible-managed system as a user account other than root.
  [#9004](https://pulp.plan.io/issues/9004)


Misc
----

- [#9007](https://pulp.plan.io/issues/9007)


----


3.14.1 (2021-07-08)
===================


No significant changes.


----


3.14.0 (2021-07-01)

Features
--------

- Add git repo and revision to pulcore and plugin installer.
  [#6547](https://pulp.plan.io/issues/6547)
- Create or import a key for pulp-api to use when encrypting sensitive db fields. Introduces new variables `pulp_db_fields` & `pulp_db_fields_key_remote`.
  [#8704](https://pulp.plan.io/issues/8704)


Bugfixes
--------

- Enable installing in FIPS mode whenever installing from RPM packages (pulp_install_source == "packages"), which may be patched for FIPS mode.
  [#8834](https://pulp.plan.io/issues/8834)
- Ensure we clean the static folder before running collectstatic. This prevents
  some upgrade issues.
  [#8872](https://pulp.plan.io/issues/8872)
- Fix installation of molecule on python 2 by limiting the python 2 version of ruamel.yaml.clib to 0.2.2.
  [#8977](https://pulp.plan.io/issues/8977)


Deprecations and Removals
-------------------------

- Remove the deprecated variable pulp_install_api_service. (It was previously stated to be removed in #7005, but was actually deprecated.)
  [#8871](https://pulp.plan.io/issues/8871)


Devel
-----

- When CI runs for a tag (release), only run pip release and package tests, not source (devel) tests.
  [#6550](https://pulp.plan.io/issues/6550)
- Fix upgrade CI tests failing on Debian 10 & CentOS 8 during verification by upgrading systemd.
  [#8887](https://pulp.plan.io/issues/8887)


----


3.13.0 (2021-05-26)
===================


Features
--------

- Adding support to Fedora 34
  [#8688](https://pulp.plan.io/issues/8688)


Bugfixes
--------

- Append missing slash to the token_server path.
  [#8763](https://pulp.plan.io/issues/8763)


Improved Documentation
----------------------

- Provide a much better explanation of customizing your installation, and how to use variables, in the new documentation section "Customizing Your Pulp Deployment".
  [#8552](https://pulp.plan.io/issues/8552)


Devel
-----

- Adding release script
  [#7961](https://pulp.plan.io/issues/7961)


----


3.12.2 (2021-04-30)
===================


Bugfixes
--------

- On some environments we need to escalate privilege for Enumerate default system PATH.
  [#8186](https://pulp.plan.io/issues/8186)
- Only listen IPv6 when it is configured on the managed host
  [#8536](https://pulp.plan.io/issues/8536)


Improved Documentation
----------------------

- Add more details to & update the "System Requirements" section of the docs.
  [#8551](https://pulp.plan.io/issues/8551)


----


3.12.1 (2021-04-21)
===================


Bugfixes
--------

- Fixed a bug where workers did not scale down.
  [#8490](https://pulp.plan.io/issues/8490)
- Replace yum pulpcore repository base url from
  https://fedorapeople.org/groups/katello/releases/yum/nightly/pulpcore/
  to https://yum.theforeman.org/pulpcore/
  [#8586](https://pulp.plan.io/issues/8586)


Improved Documentation
----------------------

- Add workaround to install redis correctly
  [#7773](https://pulp.plan.io/issues/7773)
- Add hardware requirement link to docs. General doc cleanup.
  [#8477](https://pulp.plan.io/issues/8477)


----


3.12 (2021-04-09)
=================


Features
--------

- Vagrant environment: Created a pair of Pulp 2 / Pulp 3 FIPS boxes, pulp2-nightly-pulp3-source-fips-a (Pulp 3 FIPS **VM**)
  & pulp2-nightly-pulp3-source-fips-b (Pulp 2 FIPS **container** that runs **on top** of the "a" VM.)
  [#8097](https://pulp.plan.io/issues/8097)
- Allow specifying file upload limit
  [#8212](https://pulp.plan.io/issues/8212)
- Install object storage support (azure/s3)
  [#8446](https://pulp.plan.io/issues/8446)
- Introduce advanced variable: ``pulp_service_timeout``
  [#8498](https://pulp.plan.io/issues/8498)


Bugfixes
--------

- Avoid using shared variables from pulp_database role
  [#8519](https://pulp.plan.io/issues/8519)


Devel
-----

- Configure pulp-cli at devel role
  [#8416](https://pulp.plan.io/issues/8416)
- Adding required collections to requirement.yml
  [#8443](https://pulp.plan.io/issues/8443)


----


3.11.2 (2021-05-26)

No significant changes.


----


3.11.1 (2021-04-30)
===================


Bugfixes
--------

- Only listen IPv6 when it is configured on the managed host
  [#8536](https://pulp.plan.io/issues/8536)


----


3.11.1 (2021-04-30)
===================


Bugfixes
--------

- Only listen IPv6 when it is configured on the managed host
  [#8536](https://pulp.plan.io/issues/8536)


----


3.11.0 (2021-03-16)
===================


Features
--------

- The `pulp_content_workers` option can be used to adjust the number of Gunicorn worker processes handling content app requests.
  [#8267](https://pulp.plan.io/issues/8267)
- Adding ansible 3 support
  [#8365](https://pulp.plan.io/issues/8365)


Bugfixes
--------

- Fix Pulp clients experience "connection timed out" on very slow machines, such as Qemu emulated machines, by raising the the Pulp server's gunicorn worker timeout to 90 seconds.
  [#8228](https://pulp.plan.io/issues/8228)
- Fix pulp_installer, on SELinux-enabled systems, not being idemopotent and always restoring SELinux contexts.
  [#8281](https://pulp.plan.io/issues/8281)


Improved Documentation
----------------------

- Adds documentation to pulplift.md on how to configure a Vagrant box on an HDD.
  [#8285](https://pulp.plan.io/issues/8285)


Deprecations and Removals
-------------------------

- Require postgreSQL >= 10 due to FIPS
  Upgrade postgreSQL 9.6 to postgreSQL 10 on CentOS 7
  [#8154](https://pulp.plan.io/issues/8154)
- FIPS support is removed due to Django (a dependency of Pulp) not being FIPS compatible.
  [#8258](https://pulp.plan.io/issues/8258)
- Removing ansible 2.8 support
  [#8365](https://pulp.plan.io/issues/8365)


Misc
----

- [#8337](https://pulp.plan.io/issues/8337)


Devel
-----

- Re-implement FIPS CI and enable future SELinux CI by using Qemu Emulation on Github Actions.
  [#7884](https://pulp.plan.io/issues/7884)
- Fix compatibility with ansible-lint 5.0.0 by having it not check requirements.yml under the molecule directories.
  [#8234](https://pulp.plan.io/issues/8234)
- The dev role patches Django to allow continued FIPS compatibility development within Pulp in preparation for Django to add FIPS support at some point.
  [#8258](https://pulp.plan.io/issues/8258)


----


3.10.0 (2021-02-04)
===================


Features
--------

- Added support for upgrading to pulpcore 3.10.

  The installer moves an existing 'artifact' directory inside the MEDIA_ROOT path.
  [#8011](https://pulp.plan.io/issues/8011)


Misc
----

- [#8210](https://pulp.plan.io/issues/8210)

----


3.9.1-1 (2021-01-27)
====================


Features
--------

- Install the Linux distro's `gpg` binary command for the new SigningService functionality in pulpcore.
  [#8163](https://pulp.plan.io/issues/8163)


Bugfixes
--------

- Fix the installer (versioned 3.9.1-x) still installing pulpcore 3.9.0 instead of 3.9.1.
  [#8158](https://pulp.plan.io/issues/8158)


----


3.9.1 (2021-01-21)
==================


Features
--------

- Add support for Fedora 33.
  [#7800](https://pulp.plan.io/issues/7800)
- Introduce the new variable `pulp_firewalld_zone` so that users can manually specify the firewalld zone to open up to Pulp traffic.
  [#8107](https://pulp.plan.io/issues/8107)


Bugfixes
--------

- When upgrading from distro packages (`pulp_install_source==packages` & `pulp_pkg_upgrade_all==true`), pulp_installer will now configure dnf (CentOS/RHEL 8) to permit upgrading them to newer versions that are not necessarily the latest (dnf option `best=false`). This addresses the issue of python3-rq from EPEL8 being too new for Pulp, and thus upgrades failing with a depsolve error on the task "pulp_common : Upgrade all existing installed Pulp packages".
  [#8042](https://pulp.plan.io/issues/8042)


----


3.9.0-1 (2020-12-17)
====================


Bugfixes
--------

- Fixed inability to install on CentOS 8.3 or CentOS Stream due to the newly renamed "powertools" repo
  (formerly "PowerTools") not being enabled by the installer.
  [#7996](https://pulp.plan.io/issues/7996)


Misc
----

- [#7841](https://pulp.plan.io/issues/7841)


----


3.9.0 (2020-12-07)
==================


Features
--------

- Updated gunicorn access log format to include correlation id in the pulpcore api service file.
  [#7792](https://pulp.plan.io/issues/7792)


Bugfixes
--------

- Fixed apache config to handle unix sockets.
  [#7524](https://pulp.plan.io/issues/7524)


Improved Documentation
----------------------

- Added documentation how to use the pulplift vagrant facilities.
  [#7878](https://pulp.plan.io/issues/7878)


Misc
----

- [#4968](https://pulp.plan.io/issues/4968), [#6752](https://pulp.plan.io/issues/6752)


----


3.8.1-1 (2020-11-09)
====================


Bugfixes
--------

- Fixed Ansible error with loop variables when deploying webserver configuration snippets to apache.
  [#7746](https://pulp.plan.io/issues/7746)
- Fix SELinux denials on symlinking by the galaxy_ng content plugin by updating pulpcore-selinux (SELinux policies) to 1.2.3.
  [#7780](https://pulp.plan.io/issues/7780)


Improved Documentation
----------------------

- Configured `content_origin' to properly choose between `http` and `https` in the example playbooks as well as the vagrant playbooks.
  [#7798](https://pulp.plan.io/issues/7798)


Misc
----

- [#7804](https://pulp.plan.io/issues/7804)


----


3.8.1 (2020-11-02)
==================


Features
--------

- Added a pulpcore-manager wrapper to setup the environment and call the real pulpcore-admin command as pulp user.
  [#7155](https://pulp.plan.io/issues/7155)
- Migrated Vagrant infrastructure from pulplift to this repository.
  [#7527](https://pulp.plan.io/issues/7527)


Bugfixes
--------

- Added become and proper condition to SELinux handlers.
  This fixes an issue with installations that are not run as root.
  [#7736](https://pulp.plan.io/issues/7736)


Misc
----

- [#6753](https://pulp.plan.io/issues/6753)


----


3.8.0 (2020-10-21)
==================


Features
--------

- Compile and install the pulpcore-selinux policy on CentOS/RHEL/Fedora.
  [#7574](https://pulp.plan.io/issues/7574)
- When installing from distro packages (`pulp_install_source==packages`), from a repo (`pulp_pkg_repo`), and upgrading them (`pulp_pkg_upgrade_all==true`), pulp_installer will now upgrade all the packages from the repo. This addresses any incorrect dependency declarations in the repo, which would cause pulp_installer to fail on collectstatic.
  [#7646](https://pulp.plan.io/issues/7646)
- Allow one to customize webserver ports pulp will be listening on via `pulp_webserver_http_port`
  (defaults to 80) and `pulp_webserver_https_port` (defaults to 443).
  [#7662](https://pulp.plan.io/issues/7662)
- Start rq & gunicorn from the bash wrapper scripts provided by newer pulpcore 3.7 RPM packages, `/usr/libexec/pulpcore/{rq,gunicorn}`. These scripts enable pulp processes to transitioning to the Pulp SELinux context, rather than the generic rq/gunicorn context.
  [#7667](https://pulp.plan.io/issues/7667)


Deprecations and Removals
-------------------------

- pulp_installer will no longer set SELinux to enabled, permissive and enforcing (casually referred to as "disabled") on CentOS/RHEL/Fedora.
  [#7573](https://pulp.plan.io/issues/7573)
- pulp_installer no longer supports installing from older RPM packages that lack the wrapper scripts `/usr/libexec/pulpcore/{rq,gunicorn}`.
  [#7667](https://pulp.plan.io/issues/7667)


Misc
----

- [#7709](https://pulp.plan.io/issues/7709)


----


3.7.8 (2021-08-25)

No significant changes.


----


3.7.7-1 (2021-07-30)
====================


Misc
----

- Adding `requires_ansible` metadata [#8337](https://pulp.plan.io/issues/8337)


----


3.7.7 (2021-07-28)
==================


Features
--------

- Add git repo and revision to pulcore and plugin installer.
  [#6547](https://pulp.plan.io/issues/6547)


Bugfixes
--------

- Fix the "markuppy" `pkg_resources.DistributionNotFound` error on the task
  `pulp_common : Collect static content`.
  This occurs when installing from RPM packages on EL8 (ever since EPEL8 released
  python-tablib-3.0.0-1.el8 on approximately 2021-07-23).
  [#9166](https://pulp.plan.io/issues/9166)
- If you upgrade from older pulpcore to pulpcore 3.7 from RPMs, `pulp_common: Collect static content` may fail due to dynaconf being too old (3.0.0rc1 is older than 3.0.0 final). If this happens, you can now workaround it by setting `pulp_pkg_upgrade_all: true` (or upgrading the RPM "python3-dynaconf").
  [#9181](https://pulp.plan.io/issues/9181)


----


3.7.6 (2021-04-29)
==================


No significant changes.


----


3.7.5 (2021-04-12)
==================


No significant changes.


----


3.7.4 (2021-03-16)
==================


Features
--------

- Install the Linux distro's `gpg` binary command for the new SigningService functionality in pulpcore.
  [#8406](https://pulp.plan.io/issues/8406)


Bugfixes
--------

- Fixed inability to install on CentOS 8.3 or CentOS Stream due to the newly renamed "powertools" repo
  (formerly "PowerTools") not being enabled by the installer.
  [#8407](https://pulp.plan.io/issues/8407)


----


3.7.3 (2020-10-29)
==================


Bugfixes
--------

- Backport of a bug fix to import EPEL GPG keys before using EPEL. This is needed due to a recent change in ansible.
  [#7769](https://pulp.plan.io/issues/7769)


----

3.7.2 (2020-10-21)
==================


No significant changes.


----


3.7.1 (2020-09-30)
==================


Bugfixes
--------

- Fixed Apache config bug that prevented Pulp 2 API from being accessible.
  [#7481](https://pulp.plan.io/issues/7481)


----


3.7.0 (2020-09-23)
==================


Features
--------

- Install patched dependencies that are modified for FIPS compatibility on Red Hat based operating systems. Additionally remove ``md5`` from the ``ALLOWED_CONTENT_CHECKSUMS`` setting. Users can override the ``ALLOWED_CONTENT_CHECKSUMS`` if a new value is provided.
  [#6988](https://pulp.plan.io/issues/6988)


Bugfixes
--------

- Changed the mechanism to only set the admin password on first installation.
  Removed the depedency of ``pulp_health_check`` on the variable ``pulp_default_admin_password``.
  [#7499](https://pulp.plan.io/issues/7499)


Devel
-----

- pulp_devel role now installs distro-specific packages in parallel, for better performance when run against hosts running multiple distros (like our molecule CI).
  [#7516](https://pulp.plan.io/issues/7516)
- pulp_installer's CI/molecule "packages mode" tests now test a new Foreman/Katello project URL for RPM packages. Has pulpcore 3.6 rather than 3.4.
  [#7517](https://pulp.plan.io/issues/7517)


----


3.6.3-1 (2020-09-15)
====================


Bugfixes
--------

- Changed pulp users main group from 'users' to '{{ pulp_group }}'.
  [#7173](https://pulp.plan.io/issues/7173)
- Fix auth migrations being run for galaxy_ng. Due to code removal, the
  pulp_default_admin_password is now set whenever pulpcore is 1st installed, updated/upgraded,
  or when `pulp_upgraded_manually==true`.
  [#7493](https://pulp.plan.io/issues/7493)
- Fix upgrades from pulpcore 3.0 failing at collectstatic by upgrading dynaconf to at least 3.1.1rc2.
  [#7503](https://pulp.plan.io/issues/7503)


Devel
-----

- Install pulp-rpm in the RPM package molecule / CI tests. (In addition to pulp-file.)
  [#7455](https://pulp.plan.io/issues/7455)
- Molecule & pulp_installer CI no longer update the CentOS 8 container to CentOS Stream.
  (They were doing it always, since 8.2 released by accident.)
  [#7456](https://pulp.plan.io/issues/7456)
- CI: Do not install dnf on CentOS 7. So as to actually test yum (yum 3), like most users use.
  [#7473](https://pulp.plan.io/issues/7473)


----


3.6.5 (2020-11-11)
==================


This new version of pulp_installer only differs in that it installs the new version 3.6.5.post2 of pulpcore.


----


3.6.4 (2020-09-23)
==================


No significant changes, and is created as a compatibility release that can install pulpcore 3.6.4.


----


3.6.2 (2020-09-02)
==================


No significant changes.


----


3.6.1 (2020-09-02)
==================


Bugfixes
--------

- Restart services after collect static
  [#7366](https://pulp.plan.io/issues/7366)
- Fixed bug where pulp_install_plugins source_dir vcs was being used when checking depdencies via pip-compile
  [#7382](https://pulp.plan.io/issues/7382)


----


3.6.0-1 (2020-08-20)
====================


Bugfixes
--------

- pulp_installer now uses ansible_facts namespaced vars instead of relying on `INJECT_FACTS_AS_VARS=True <https://docs.ansible.com/ansible/latest/reference_appendices/config.html#inject-facts-as-vars>`_.
  [#7322](https://pulp.plan.io/issues/7322)
- Assuring to restart only pulpcore services
  [#7334](https://pulp.plan.io/issues/7334)
- Fix template for pulp_health_check
  [#7335](https://pulp.plan.io/issues/7335)
- Accept unix socket on pulp_health_check
  [#7349](https://pulp.plan.io/issues/7349)
- Fix failure on task "pulp_common: Make /var/lib/pulp world executable" by creating the directory
  (and giving it owner user permissions as well). Occurs when specifying an existing user account
  as pulp_user but not having /var/lib/pulp (`pulp_user_home`) already present. pulplift would
  trigger this.
  [#7359](https://pulp.plan.io/issues/7359)


Deprecations and Removals
-------------------------

- The default location for Pulp Webserver's TLS certificates was changed from /etc/pulp to /etc/pulp/certs/ .
  Users that wish to continue using their current certificate and key must run
  `sudo mv -t /etc/pulp/certs/ /etc/pulp/pulp_webserver.{key,crt}` before upgrading / running
  the new pulp_installer version. Alternatively, users can control the directory with the variable
  `pulp_certs_dir`, which was renamed from `pulp_webserver_tls_folder`. `pulp_certs_dir` now also
  controls where the keys for API authentication tokens are installed as well.
  [#7328](https://pulp.plan.io/issues/7328)


----


3.6.0 (2020-08-13)
==================


Features
--------

- Allow an installer user to configure Pulp to run with TLS enabled using custom provided
  certificates.
  [#6845](https://pulp.plan.io/issues/6845)
- Misc webserver changes so that Let's Encrypt and other ACME protocol CAs can be used via 3rd-party ansible roles, primarily for HTTP-01 verification. See docs/letsencrypt.md for a full HTTP-01 example playbook and explanation.
  [#6846](https://pulp.plan.io/issues/6846)
- Allow an installer user to configure Pulp to run with TLS enabled using self-signed certificates.
  [#6847](https://pulp.plan.io/issues/6847)
- A key for token authentication is installed from either a specified file or a newly generated one.
  [#7098](https://pulp.plan.io/issues/7098)
- Enable resource accounting via systemd.
  [#7192](https://pulp.plan.io/issues/7192)
- Verify if Pulp Services are up & listening
  [#7259](https://pulp.plan.io/issues/7259)


Bugfixes
--------

- Fix the tasks "Install pulpcore via PyPI" & "Install Pulp plugins via PyPI" always reporting CHANGED when pip 20.2 is installed.
  [#7254](https://pulp.plan.io/issues/7254)
- Fix services not starting due to pulp_installer putting the wrong path to binaries like gunicorn in
  systemd unit files. Only occured when installing in packages mode.
  [#7255](https://pulp.plan.io/issues/7255)
- Fix pulp_installer failing on the task "pulp_common: Add pulpcore RPM repositories" when installing
  in packages mode, and when ansible_user is not root.
  [#7275](https://pulp.plan.io/issues/7275)
- Fix pulp_installer failing on task "pulp_webserver : Set httpd_can_network_connect flag on and keep
  it persistent across reboots" on hosts with SELinux enabled (enforcing/permissive) by installing
  the SELinux python RPM dependencies.
  [#7276](https://pulp.plan.io/issues/7276)


Deprecations and Removals
-------------------------

- Remove the systemd sandboxing features from the pulpcore-api systemd unit file. This was preventing pulpcore-api from starting on containers running systemd (due to namespace capabilities), such as our molecule tests & CI.
  [#6586](https://pulp.plan.io/issues/6586)
- Installations will have https enabled by default. Users need to configure their CONTENT_ORIGIN accordingly.
  [#6845](https://pulp.plan.io/issues/6845)


Misc
----

- [#6047](https://pulp.plan.io/issues/6047), [#7230](https://pulp.plan.io/issues/7230)


Devel
-----

- Fix molecule (CI or local) often failing to test more than 1 OS a time.
  [#7263](https://pulp.plan.io/issues/7263)
- Add verification that Pulp is running at the end of pulp_installer CI, via inspec.
  [#7272](https://pulp.plan.io/issues/7272)


----


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

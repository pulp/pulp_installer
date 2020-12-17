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

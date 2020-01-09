Pulp
====

Ansible role that installs Pulp 3 from PyPi or source and provides config.

The default administrative user for the Pulp application is: 'admin'

Role Variables:
---------------
* `pulp_cache_dir`: Location of Pulp cache. Defaults to "/var/lib/pulp/tmp".
* `pulp_config_dir`: Directory which will contain Pulp configuration files.
  Defaults to "/etc/pulp".
* `pulp_default_admin_password`: Initial password for the Pulp admin. **Required**.
* `pulp_install_dir`: Location of a virtual environment for Pulp and its Python
  dependencies. Defaults to "/usr/local/lib/pulp".
* `pulp_install_plugins`: A nested dictionary of plugin configuration options.
  Defaults to "{}", which will not install any plugins.
  * Dictionary Key: The pip installable plugin name. This is defined in each
  plugin's* `setup.py`. **Required**.
  * `update`: Whether to update/upgrade the plugin to the latest stable release from PyPI. To limit this to micro (z-stream) updates, make sure to set `branch`. Note that if the latest stable release of the plugin is incompatible with `pulp_branch`, ansible-pulp will fail (and exit the play) when it goes to update the plugin. Defaults to "false".
  * `version`: Optional. A specific version of the plugin to install from PyPI. Ignored if `source_dir` is set. Overrides `update` to `true`.
  * `branch`: Optional: A specific branch of the plugin to install from PyPI (or update/upgrade to the latest release from, see `update`). An example value is "1.0". Ignored if `source_dir` or `version` is set. You need to set this to a branch that is compatible with either `pulp_branch` or `pulp_version`, if they are set.
  * `source_dir`: Optional. Absolute path to the plugin source code. If present,
  plugin will be installed from source in editable mode.
  Also accepts a pip VCS URL, to (for example) install the master branch.
  * `prereq_role`: Optional. Name of (or folder path to) Ansible role to run
    immediately before the venv is created. You will need to download it 1st (with
    ansible-galaxy.) Needed because many plugins will have OS dependencies in C.
    See `prereq_pip_packages` also.
* `pulp_install_api_service`: Whether to create systemd service files for
  pulpcore-api. Defaults to "true".
* `pulp_update`: Whether to update/upgrade pulpcore to the latest stable release from PyPI within `pulp_branch`. Only affects systems where Pulp is already installed. To limit this to micro (z-stream) updates, make sure to set `pulp_branch`. If `pulpcore_version` is set, or `pulp_source_dir` is set, this has no effect and is effectively always `true`. Defaults to "false".
* `pulp_branch`: The branch of of pulpcore (or update/upgrade to the latest release from, see `pulp_update`). Defaults to the latest stable branch release of pulpcore at the time of ansible-pulp being released, which is currently `3.0`. It is recommended to set this if you ever plan to re-run the ansible installer; when a new branch is released and if you update ansible-pulp, some of your content plugins may not be compatible yet. An example value is `3.1`. Ignored if `pulp_source_dir` or `pulp_version` is set. Do not set this to a version higher than the current default (unless you are installing a development branch of pulpcore, and have updated ansible-pulp 1st.)
* `pulp_version`: Optional. A specific version of pulp to install from PyPI. Ignored if `pulp_source_dir` is set. Overrides `pulp_update` to `true`.
* `pulp_source_dir`: Optional. Absolute path to pulpcore source code. If
  present, pulpcore will be installed from source in editable mode. Also accepts
  a pip VCS URL, to (for example) install the master branch, or an arbitrary commitish (tag, branch, commit, etc.)
* `pulp_user`: User that owns and runs Pulp. Defaults to "pulp".
* `pulp_user_id`: Integer value of uid for the `pulp_user`. Defaults to nothing and uid is assigned
  by the system.
* `pulp_group`: The group that the `pulp_user` belongs to. Defaults to `pulp`.
* `pulp_group_id`: Integer value of gid for the `pulp_group`. Defaults to nothing and gid is
  assigned by the system.
* `pulp_extra_groups`: Optional. A list of additional group names that the `pulp_user` should
  be added to. This is site-specific and defaults to nothing.
* `pulp_use_system_wide_pkgs` Use python system-wide packages. Defaults to "false".
* `pulp_remote_user_environ_name` Optional. Set the `REMOTE_USER_ENVIRON_NAME` setting for Pulp.
  This variable will be set as the value of `CONTENT_HOST` as the base path to build content URLs.
* `pulp_api_bind` Interface and Port where Pulp Content `gunicorn` service will listen. Defaults to
  '127.0.0.1:24817'. This variable is the value used to render the `pulpcore-api.service.j2` template
  passing to the `--bind` parameter of the `gunicorn` service.
* `pulp_settings`: A nested dictionary that is used to add custom values to the user's
    `setting.py`, which will override any default values set by pulpcore. The keys of this
    dictionary are variable names, and the values can be nested. Please see [pulpcore configuration
    docs](https://docs.pulpproject.org/en/3.0/nightly/installation/configuration.html#id2) for
    documentation on the possible values.
  * `pulp_settings.content_origin`: **Required**. The URL to the pulp-content
    host that clients will access, and that will be appended to in HTTP
    responses by multiple content plugins. Any load balancers / proxies (such
    as those in the `pulp-webserver` role) normally should be specified instead
    of the pulp content host itself. Syntax is
    `(http|https)://(hostname|ip)[:port]`.
  * `pulp_settings.secret_key`: **Required**. Pulp's Django application `SECRET_KEY`.
* `epel_release_packages`: List of strings (package names, URLs) to pass to
  `yum install` to ensure that "epel-release" is installed.
  Once the 1st string is found to be installed by yum, no further strings are
  attempted.
  Defaults to (on el7 for example): ["epel-release", "https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm"]
  Set to an empty list `[]` if you wish to disable trying to install
  epel-release, such as if you manually add the EPEL repo via your own
  configuration or subscription-manager/katello.
  Also accepts a single string or empty string.
  Only affects CentOS/RHEL.
* `rhel7_optional_repo`: List of possible names for the rhel7 optional repo
  to enable. Once the 1st name is enabled (or found to already be enabled),
  no further names are attempted.
  Defaults to  ["rhui-rhel-7-server-rhui-optional-rpms", "rhel-7-server-optional-rpms", "rhel-7-workstation-optional-rpms"]
  Set to an empty list `[]` if you wish to disable trying to enable the repo,
  such as if you manually add the optional repo via your own configuration or
  subscription-manager/katello.
  Also accepts a single string or empty string.
  Only affects RHEL7 (RHEL8 no longer has an optional repo.)

Shared Variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

* `prereq_pip_packages`: Additional pip packages to install in the virtual
  environment before installing pulp or its content plugins.
  Defaults to an empty list, but a `prereq_role` may append to it.

This role is required by the `pulp-database` role and uses some variables from it.

* `pulp_settings_db_defaults`: See pulp-database README.


Operating System Variables:
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

Idempotency:
------------
This role is idempotent by default. It is dependent on these settings remaining `false`:
* `pulp_update`
* Every `update` under `pulp_install_plugins`

Note on Plugin Version Compatibility with Pulpcore
--------------------------------------------------

Pulp 3 has a plugin architecture so that new content types, and new features, can be added by the larger community. However, both pulpcore & plugins are installed via pip, which has limited dependency resolution. Plugins release at their own lifecycles. Thus in the worst case scenario, the 2 stable branches of plugin pulp_juicy could depend on the current branch of pulpcore, while the 2 stable branches of pulp_sugary could depend on the current branch of pulpcore.

In order to avoid breaking multiple plugins for the sake of 1 plugin, and to avoid breaking existing installs, updating a plugin will not cause pulpcore to be updated as dependency. Similarly, if a plugin were to be attempted to be updated to an incompatible version with pulpcore, the installer will fail & exit.

Thus you, yourself, must research plugin compatibility with pulpcore whether you are installing 1 plugin, or more than 1 plugin.

Suggested Workflows for Pulpcore & Plugin Versioning:
-----------------------------------------------------

### Latest versions with minimal work:

Initial install:

1. Observe the latest branch of pulpcore (3.0).
2. Confirm that all the latest stable releases of your desired plugins are compatibile with pulpcore 3.0, such as by reading their README.md.
3. Do not set `pulp_branch`. Do not set `branch` under `pulp_install_plugins`.
4. Run ansible-pulp.

Updating your install:

1. Check if `pulp_branch` has changed to a new stable branch in the latest version of the installer. This will happen whenever a new branch of `pulpcore` is released. Let's assume 3.0 is stil the latest, but there are new micro updates (like pulpcore 3.0.3 -> 3.0.4, and pulp_juicy 1.0.3 -> 1.0.4)
2. Update ansible-pulp
3. re-run the ansible-pulp with `update` set to `true` under `pulp_install_plugins`, and `pulp_update` set to `true`.

Upgrading your install:

1. Check if `pulp_branch` has changed to a new stable branch in the latest version of the installer. This will happen whenever a new branch of `pulpcore` is released. Let's assume 3.1 is released.
2. Check if your plugins are compatible yet with pulpcore 3.1 yet. **Wait** for the plugins to be updated for compatibility if they are not updated yet before you attempt to update.
3. If they are updated for compatibility:
    1. Update ansible-pulp
    2. re-run the ansible-pulp with `update` set to `true` under `pulp_install_plugins`, and `pulp_update` set to `true`.

### Specifying your desired branch:

Initial install:

1. Observe the latest branch of pulpcore (3.0).
2. Confirm that all the latest stable releases of your desired plugins are compatibile with pulpcore 3.0, such as by reading their README.md. If they are not all compatible, look into whether the older version is compatible. If not, try an even older version. Let's assume the newest version compatible with all is called `X.Y`.
3. Set `pulp_branch` to `X.Y`. Set `branch` under each of the  `pulp_install_plugins` to their own compatible semantic minor branch versions `a.b`.
4. Run ansible-pulp

Updating your install:

1. Check if `pulp_branch` has changed to a new stable branch in the latest version of the installer. This will happen whenever a new branch of `pulpcore` is released. Let's assume 3.0 is stil the latest, but there are new micro updates (like pulpcore 3.0.3 -> 3.0.4, and plugin pulp_juicy 1.0.3 -> 1.0.4)
2. Update ansible-pulp
3. re-run the ansible-pulp with `update` set to `true` under `pulp_install_plugins`, and `pulp_update` set to `true`.

Upgrading your plugins, but not pulpcore:

1. Check if `pulp_branch` has changed to a new stable branch in the latest version of the installer, and if new branches of the plugins have been released. This will happen whenever a new branch of `pulpcore` is released. Let's assume 3.0 is still the latest branch of pulpcore.
2. Repeat step 2 from the initial install. Let's assume that , but pulp_juicy has gone to a new branch (pulp_juicy 1.0.3 -> 2.0.0) with major new features, while still being compatible with your pulpcore version (3.0).
3.`Change pulp_install_plugins.pulp_juicy.branch` to `2.0`. This is its new current & perpetual value.
4. set `pulp_install_plugins.pulp_juicy.update` to `true`; it will upgrade it. Set `pulp_update` to true as a precaution for the latest bugfixes  that the plugins may depend on.
5. Update ansible-pulp
6. Run ansible-pulp

Upgrading your plugins, and pulpcore:

1. Check if `pulp_branch` has changed to a new stable branch in the latest version of the installer, and if new branches of the plugins have been released. This will happen whenever a new branch of `pulpcore` is released. Let's assume 3.0 is still the latest branch of pulpcore.
2. Repeat step 2 from the initial install. Let's assume that pulpcore is now on branch 3.1, and pulp_juicy has gone to a new minor branch (pulp_juicy 2.0.0 -> 3.0.0) for compatibility purposes with pulpcore version 3.1. All your other plugins have as well.
3. set `pulp_install_plugins.pulp_juicy.update` to `true`; it will upgrade it. Set `update` for all your other `pulp_install_plugins` as well. Set `pulp_update` to true; it will upgrade pulpcore.
4.`Change pulp_install_plugins.pulp_juicy.branch` to `2.0`. This is its new current & perpetual value. Repeat with the correct values you determined for `branch` for all the other `pulp_install_plugins`.
5. Update ansible-pulp
6. Run ansible-pulp

License
-------

GPLv2

Author Information
------------------

Pulp Team

Pulp Common
===========

Ansible role that installs shared components of the Pulp 3 services from PyPi or source and provides basic config.

The default administrative user for the Pulp application is: 'admin'

Role Variables
--------------
* `pulp_install_plugins`: **Required** A nested dictionary of plugins to install & their
  installation options.
    * *Dictionary Key*: **Required**. The pip installable plugin name. This is defined in each
    plugin's `setup.py`.
    * `version`: Specific release of the plugin to install from PyPI initially, or to upgrade to.
    If `source_dir` is set, this has no effect. Note that if the specified release of the plugin is
    incompatible with pulpcore's version, pulp_installer will fail (and exit the play) before it
    tries to install or upgrade the plugin. Defaults to nothing, which means the latest release from
    PyPI will be installed initially, and no upgrades will be performed unless `upgrade` is set.
    * `version` and `upgrade` **cannot be used together**. Even though a command like `pip install
    --upgrade pulp-file=0.3.0` is valid, the ansible pip module refuses to let you specify version
    and `state=latest` (`state=latest` maps to `pip --upgrade`, and to our upgrade: true).
    * `upgrade`: Whether to update/upgrade the plugin to the latest stable release from PyPI.
    Only affects systems where the plugin is already installed. If `source_dir` is set,
    this has no effect and is effectively always `true`. Mutually exclusive with `version`.
    Note that if the latest stable release of the plugin is incompatible with pulpcore's version,
    pulp_installer will fail (and exit the play) when it goes to upgrade the plugin.
    Defaults to "false".
    * `source_dir`: Optional. Absolute path to the plugin source code. If present,
  plugin will be installed from source in editable mode.
  Also accepts a pip VCS URL, to (for example) install the master branch.
    * `prereq_role`: Optional. Name of (or folder path to) Ansible role to run
    immediately before the venv is created. You will need to download it 1st (with
    ansible-galaxy.) Needed because many plugins will have OS dependencies in C.
    See `prereq_pip_packages` also.
    * `collectstatic`: Optional. Boolean that specifies if the static for a plugin should be collected.
    If set to false the plugin name will be passed as `--ignore` at collectstatic time.
    * **Example**:
    ```yaml
    pulp_install_source: pip
    pulp_install_plugins:
      pulp-zero: {}
      pulp-one: # plugin name (pulp-ansible, pulp-container, pulp-rpm, ...)
        version: "1.0.1" # specific release (pulp-file-0.3.0)
      pulp-two:
        upgrade: true # upgrade to the latest stable release from PyPI
      pulp-three:
        source_dir: "/var/lib/pulp/pulp_three" # path to the plugin source code
      pulp-four:
        prereq_role: "pulp.pulp_four_role" # role to run immediately before the venv is created
      pulp-five:
        collectstatic: false
    ```
* `pulp_cache_dir`: Location of Pulp cache. Defaults to "/var/lib/pulp/tmp".
* `pulp_config_dir`: Directory which will contain Pulp configuration files.
  Defaults to "/etc/pulp".
* `pulp_install_dir`: Location of a virtual environment for Pulp and its Python
  dependencies. Defaults to "/usr/local/lib/pulp".
* `pulp_user_home`: equivalent to `MEDIA_ROOT` from `pulpcore` i.e. absolute path for pulp user home.
* `pulp_source_dir`: Optional. Absolute path to pulpcore source code. If
  present, pulpcore will be installed from source in editable mode. Also accepts
  a pip VCS URL, to (for example) install the master branch.
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
* `pulp_settings`: A nested dictionary that is used to add custom values to the user's
    `setting.py`, which will override any default values set by pulpcore. The keys of this
    dictionary are variable names, and the values should be expressed using the [Dynaconf syntax](
    https://dynaconf.readthedocs.io/en/latest/guides/environment_variables.html#precedence-and-type-casting)
    Please see [pulpcore configuration
    docs](https://docs.pulpproject.org/en/master/nightly/installation/configuration.html#id2) for
    documentation on the possible variable names and their values.
  * `pulp_settings.content_origin`: **Required**. The URL to the pulp_content
    host that clients will access, and that will be appended to in HTTP
    responses by multiple content plugins. Any load balancers / proxies (such
    as those in the `pulp_webserver` role) normally should be specified instead
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
* `pulp_certs_dir`: Path where to generate or drop the TLS certificates & keys for authentication
  tokens. Not used directly by pulp_common, but by roles that depend on it. Defaults to
  '{{ pulp_config_dir }}/certs' .

Role Variables if installing from RPMs
--------------------------------------
Normally, Pulp is installed from Python pip packages (from PyPI.) pulp_installer can install Pulp from
RPM packages instead if this variable is set. Other distro packaging formats may work as well:

* `pulp_install_source`: Whether to install from "pip" (PyPI, python packages) or the Linux distro's
  (RPM) "packages".
  Defaults to "pip".

If it is set to "packages", the following variables are used, or behave *differently* from above:

* `pulp_install_plugins`: **Required** A nested dictionary of plugins to install & their installation options.
    * *Dictionary Key*: **Required**. The plugin name.
    * `pkg_name`: If this is left undefined, each Linux distro package will be installed by the name `pulp_pkg_name_prefix`
    with the Dictionary Key appended to it. `pulp_pkg_name_prefix` defaults to "python3-", so if the Dictionary key is
    "pulp-file", the package `python3-pulp-file` will be installed. This variable overrides the entire package name.
    * `version`: Like with pip, a user can specify a specific version of a package one wants installed.
    * **Example**:
    ```yaml
    pulp_install_source: packages
    pulp_install_plugins:
      pulp-zero: {} # Effectively python3-pulp-zero
      pulp-one:
        pkg_name: python3-pulp-one-ng
      pulp-two:
        pkg_name: pulp_two_underscores
        version: 2.2.0
    ```
* `pulp_install_dir`: Location of the filesystem prefix where package installed python programs
  (gunicorn & rq) are looked for on the filesystem.  Defaults to "/usr" (such as for "/usr/bin/gunicorn").
* `pulp_pkg_name_prefix`: The beginning of the Linux distro (RPM) package names for pulp, that is
  appended to in order to install "pulpcore" and the plugins. Defaults to "python3-".
* `pulp_pkg_pulpcore_name`: The entire name of the Linux distro (RPM) package for pulpcore.
  Defaults to: "python3-pulpcore"
* `pulp_pkg_repo`: yum/dnf package repo to add to the system before installing Pulp
  Consists simply of the URL to the repo. Defaults to nothing. Does not support any other repo
  type yet.
* `pulp_pkg_repo_gpgcheck`: Whether the package signatures should be checked or not. Defaults to `True`.
* `pulp_pkg_undeclared_deps`: Additional Linux distro (RPM) packages to install before installing pulpcore.
  See `defaults/main.yml` for default values.
* `pulp_pkg_upgrade_all`: Whether to upgrade all Pulp Linux distro (RPM) packages (including the
  `pulp_pkg_undeclared_deps` packages.)
* `pulp_upgraded_manually`: Set this to `true` if you updated/upgraded Pulp manually beforehand,
  without using the installer. (e.g., you ran `yum update` and your Pulp installation is broken. Re-running the
  installer will fix it.)
  Defaults to `false`.

Role Variables for advanced usage
---------------------------------

* `pulpcore_version`: Specify a specific version of pulpcore one would like to install or upgrade to.
   By default the installer will do the right thing by using the version of pulpcore it is designed
   for and tested with. It is strongly advised against setting.

Shared Variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

* `prereq_pip_packages`: Additional pip packages to install in the virtual
  environment before installing pulp or its content plugins.
  Defaults to an empty list, but a `prereq_role` may append to it.

This role is required by the `pulp_database` role and uses some variables from it.

* `pulp_settings_db_defaults`: See pulp_database README.

Operating System Variables
--------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

Idempotency
-----------
This role is idempotent by default. It is dependent on these settings remaining `false`:
* Every `upgrade` under `pulp_install_plugins`
* pulp_upgraded_manually

License
-------

GPLv2+

Author Information
------------------

Pulp Team

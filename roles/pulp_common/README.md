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
  Also accepts a pip VCS URL, to (for example) install the main branch.
    * `prereq_role`: Optional. Name of (or folder path to) Ansible role to run
    immediately before the venv is created. You will need to download it 1st (with
    ansible-galaxy.) Needed because many plugins will have OS dependencies in C.
    See `prereq_pip_packages` also.
    * `collectstatic`: Optional. Boolean that specifies if the static files for a plugin should be collected.
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
      pulp-six:
        source_dir: "/path/to/source/code/"
        git_url: "https://github..."  # Optional. URL to the git repo from where plugin will be pulled.
        git_revision: "v3.1.1"   # Optional. The specific git branch/tag/commit to be cheked out.
    ```
* `pulp_cache_dir`: Location of Pulp cache. Defaults to "/var/lib/pulp/tmp".
* `pulp_config_dir`: Directory which will contain Pulp configuration files.
  Defaults to "/etc/pulp".
* `pulp_install_dir`: Location of a virtual environment for Pulp and its Python
  dependencies. Defaults to "/usr/local/lib/pulp".
* `pulp_user_home`: absolute path for pulp user home.
* `pulp_media_root`: `MEDIA_ROOT` for `pulpcore`. Defaults to "/var/lib/pulp/media".
* `pulp_certs_dir`: Path where to generate or drop the TLS certificates (see pulp_webserver role) &
  keys for authentication tokens (see pulp_api role.) Also to where the user-provided gpg key for
  the galaxy-ng collection signing service is placed (see galaxy_post_install role.) Defaults to
  '{{ pulp_config_dir }}/certs' .
* `pulp_scripts_dir`: Path to where user-provided scripts (needed by specific plugins) are located.
  (see galaxy_post_install role.) Defaults to '{{ pulp_user_home }}/scripts'.
* `pulp_source_dir`: Optional. Absolute path to pulpcore source code. If
  present, pulpcore will be installed from source in editable mode. Also accepts
  a pip VCS URL, to (for example) install the main branch.
* `pulp_git_url`: Optional. URL to the git repository from where pulpcore will be checked out if
  doesn't exists already on `source_dir`.
  > **WARNING** when `pulp_git_url` is defined this role will clone the repo if doesn't already
  > exist in the `pulp_source_dir` location and also checkout/update to specified `pulp_git_revision` if
  > provided. In the case of existing local repo with unstaged changes the update will NOT be forced.
  > For development purposes the recommendation is to NOT provide `pulp_git_url` and manage local
  > branches manually.
* `pulp_git_revision`: Optional. The specific git branch/tag/commit to be cheked out
  if git_url is provided.
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
* `pulp_install_object_storage`: The preferred object storage. Defaults to `filesystem`.
* `pulp_settings`: A nested dictionary that is used to add custom values to the user's
    `settings.py`, which will override any default values set by pulpcore. The keys of this
    dictionary are variable names, and the values should be expressed using the [Dynaconf syntax](
    https://dynaconf.readthedocs.io/en/latest/guides/environment_variables.html#precedence-and-type-casting)
    Please see [pulpcore configuration
    docs](https://docs.pulpproject.org/en/main/nightly/installation/configuration.html#id2) for
    documentation on the possible variable names and their values.
  * `pulp_settings.content_origin`: **Required**. The URL to the pulp_content
    host that clients will access, and that will be appended to in HTTP
    responses by multiple content plugins. Any load balancers / proxies (such
    as those in the `pulp_webserver` role) normally should be specified instead
    of the pulp content host itself. Syntax is
    `(http|https)://(hostname|ip)[:port]`.
  * `pulp_settings.secret_key`: **Required**. Pulp's Django application `SECRET_KEY`.

* `pulp_certs_dir`: Path where to generate or drop the TLS certificates, key for authentication
  tokens, and the database fields encryption key. Defaults to '{{ pulp_config_dir }}/certs' .
* `pulpcore_update`: Boolean that specifies whether the pulpcore package should be updated to the
  latest bug fix release within the minor release specified by `pulpcore_version`. Defaults
  to `false`.
* `pulp_install_selinux_policies`: Whether or not to download & install the SELinux policies.
   This performs a operation with the `git clone` command. Accepts `True`, `False` or `auto`.
   Defaults to `auto`, which installs when SELinux is enabled (permissive or enforcing.)

Role Variables if installing from RPMs
--------------------------------------
Normally, Pulp is installed from Python pip packages (from PyPI.) pulp_installer can install Pulp from
RPM packages instead if this variable is set. Other distro packaging formats may work as well:

* `pulp_install_source`: Whether to install from "pip" (PyPI, python packages) or the Linux distro's
  (RPM) "packages".
  Defaults to "pip".

If it is set to "packages", the installer is in *packges mode*, which has the following **limitations**:

* The packages are only built for CentOS/RHEL 7 and CentOS/RHEL 8.
* Not all plugins are available from the default repo. To determine which plugins are available,
  follow [this link](https://yum.theforeman.org/pulpcore/), browse to the repo for your
  Pulp version and distribution, and search for "pulp-".
* The default repo (from yum.theforeman.org, see `pulp_pkg_repo`) is not tested for every possible
  pulpcore usage, and is thus not officially supported by the Foreman project.
* pulp_installer may install/upgrade to an older minor branch of pulpcore.
  E.g., if pulp_installer is version 3.9.z, it may install Pulp 3.8 instead. See `pulp_pkg_repo`.
* The version of Pulp installed/upgraded to may be changed to the current minor branch during any
  pulp_installer micro release.
  E.g., pulp_installer 3.9.0 may install/upgrade to Pulp 3.8, while
  pulp_installer 3.9.1 may install/upgrade to Pulp 3.9.

Furthermore, the following variables are used, or behave *differently* from above:

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
* `pulp_pkg_repo`: yum/dnf package repo to add to the system to install Pulp from.
  Consists simply of the URL to the repo. Does not support any other repo type yet.
  Defaults to either the corresponding  minor branch (3.y) repo from `yum.theforeman.org`, or an older
  minor branch. See the **limitations** above.
* `pulp_pkg_repo_gpgcheck`: Whether the package signatures should be checked or not. Defaults to `True`.
* `pulp_pkg_undeclared_deps`: Additional Linux distro (RPM) packages to install before installing pulpcore.
  See `defaults/main.yml` for default values.
* `pulp_pkg_upgrade_all`: Whether to upgrade all Pulp Linux distro (RPM) packages (including the
  `pulp_pkg_undeclared_deps` packages.)
* `pulp_upgraded_manually`: Set this to `true` if you updated/upgraded Pulp manually beforehand,
  without using the installer. (e.g., you ran `yum update` and your Pulp installation is broken. Re-running the
  installer will fix it.)
  Defaults to `false`.
* `pulp_pkg_selinux_name` The name of the package containing the SELinux policies to install. See
  `pulp_install_selinux_policies`, except `git` is not used; the package manager is used instead.
   Defaults to "pulpcore-selinux".

Role Variables for advanced usage
---------------------------------

* `pulpcore_version`: Specify a minor version of pulpcore (e.g.: `3.15`) one would like to install or upgrade to.
   By default the installer will do the right thing by using the minor version of pulpcore it is designed
   for and tested with. This can also be a specific patch release (e.g.: `3.15.2`).
* `pulp_service_timeout`: Set timeout value for pulp services. Defaults to 90.

Shared Variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

* `prereq_pip_packages`: A List of additional pip packages to install in the virtual
  environment before installing pulp or its content plugins.
  Defaults to a list containing the single item "Jinja2" (which is necessary for pulp_installer to
function). Also, a `prereq_role` may append to it.

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

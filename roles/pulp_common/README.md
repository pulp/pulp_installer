pulp_common
===========

Ansible role that installs shared components of the Pulp 3 services from PyPi or source and provides basic config.

It is a dependency of the service roles [pulp_database_config](../../roles/pulp_database_config) [pulp_api](../../roles/pulp_api), [pulp_content](../../roles/pulp_content), and [pulp_workers](../../roles/pulp_workers).

Role Variables
--------------

* `pulp_install_plugins`: **Required**. A nested dictionary of plugins to install & their
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
    * `extras`: Optional. A list of strings. Each string represents a pip "extra" dependency that
    the plugin, as a pip package, recognizes. Consult the plugin documentations for available
    extras.
    If set to false the plugin name will be passed as `--ignore` at collectstatic time.
    * **Example**:

    ```yaml
    pulp_install_source: pip
    pulp_install_plugins:
      pulp-zero:
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
        extras: # list of extra depedencies. Normally seen in pip syntax like "pulp-five[ldap,VitaminC]"
          - ldap
          - VitaminC
      pulp-six:
        source_dir: "/path/to/source/code/"
        git_url: "https://github..."  # Optional. URL to the git repo from where plugin will be pulled.
        git_revision: "v3.1.1"   # Optional. The specific git branch/tag/commit to be cheked out.
    ```

* `pulp_config_dir`: Directory which will contain Pulp configuration files.
  Defaults to "/etc/pulp".
* `pulp_install_dir`: Location of a virtual environment for Pulp and its Python
  dependencies. Defaults to "/usr/local/lib/pulp".
* `pulp_user_home`: absolute path for pulp user home. Defaults to "/var/lib/pulp".
  This variable is also default for "{{ pulp_settings.deploy_root }}, which multiple directories
  are under. Also, `pulp_scripts_dir` is placed under it.
* `pulp_certs_dir`: Path where to generate or drop the TLS certificates (see
  [pulp_webserver](../../roles/pulp_webserver) role), the keys for authentication tokens (see
  [pulp_api](../../roles/pulp_api) role), the database fields encryption key (See
  [pulp_database_config](../../roles/pulp_database_config) role). Also to where the user-provided gpg
  key for the galaxy-ng collection signing service is placed (see galaxy_post_install role.)
   Defaults to `{{ pulp_config_dir }}/certs`, which evaluates by default to `/etc/pulp/certs`.
* `pulp_scripts_dir`: Path to where user-provided scripts (needed by specific plugins) are located.
  (see [galaxy_post_install](../../roles/galaxy_post_install) role.) Defaults to `{{ pulp_user_home }}/scripts`.
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
  by the system. NOTE: It is strongly recommended to set this if doing a clustered pulp install with a
  filesystem shared (NFS) between multiple pulp hosts.
* `pulp_group`: The group that the `pulp_user` belongs to. Defaults to `pulp`.
* `pulp_group_id`: Integer value of gid for the `pulp_group`. Defaults to nothing and gid is
  assigned by the system. NOTE: It is strongly recommended to set this if doing a clustered pulp install with a
  filesystem shared (NFS) between multiple pulp hosts.
* `pulp_extra_groups`: Optional. A list of additional group names that the `pulp_user` should
  be added to. This is site-specific and defaults to nothing.
* `pulp_use_system_wide_pkgs` Use python system-wide packages. Defaults to "false".
* `pulp_remote_user_environ_name` Optional. Set the `REMOTE_USER_ENVIRON_NAME` setting for Pulp.
  This variable will be set as the value of `CONTENT_HOST` as the base path to build content URLs.
* `pulp_install_object_storage`: The preferred object storage. Defaults to `filesystem`.
* `pulpcore_update`: Boolean that specifies whether the pulpcore package should be updated to the
  latest bug fix release within the minor release specified by `pulpcore_version`. Defaults
  to `false`.
* `pulp_install_selinux_policies`: Whether or not to download & install the SELinux policies.
   This performs a operation with the `git clone` command. Accepts `True`, `False` or `auto`.
   Defaults to `auto`, which installs when SELinux is enabled (permissive or enforcing.)
* `pulp_selinux_remount_data_dir`: Whether or not to remount the pulp data directory /var/lib/pulp,
   with pulp's SELinux context (label.) This will only occur when the installer detects that
   /var/lib/pulp is its own mount point, and is listed in /etc/fstab, but cannot handle labels on
   individual files/folders (and is not already mounted with the context.) Also only occurs when
   `pulp_install_selinux_policies` is set to `true` or `auto`. Note that this functionality exists
   because the SELinux label (pulpcore_var_lib_t) does not exist on the system prior to pulp being
   installed, and certain filesystem types such as NFS cannot have labels on individual files.
   Defaults to `true`.

pulp_settings variables
-----------------------

* `pulp_install_plugins`: **Required**. A nested dictionary of plugins to install & their
* `pulp_settings`:  A dictionary that is used to add custom values to the user's
 `settings.py`, which will override any default values set by pulpcore. The keys of this
 dictionary are variable names, and the values should be expressed using the [Dynaconf syntax](
 https://dynaconf.readthedocs.io/en/docs_223/guides/environment_variables.html#precedence-and-type-casting).
 Please see [pulpcore configuration
 docs](https://docs.pulpproject.org/pulpcore/configuration/settings.html) for
 documentation on all the possible variable names and their values. Listed below are variables
 that are "Mandatory" as they have no default values, or that cannot be changed after
 installation (without manually moving files), or that the installer behaves differently based on,
 or that configure Pulp on how to talk to other servers in a cluster (and are therefore required during installation)). In all 4 cases, the variables cannot or should not merely be specified in `settings.local.py` after installation.

<!-- markdownlint-disable MD033 MD005 -->
<!-- We set wrapping for code because it's the only way to apply wrapping successfully with mkdocs. HTML tags like div, span, data etc do not work for applying wrapping
We have to set wrapping to prevent the table from becoming way to wide. It already doesn't show the entire thing, but only notes is hidden by default.-->
<style>
code
  word-wrap: break-word;
</style>

!!! note
    Scroll to the right to see all the info in the table below.

pulp_settings variable name | Mandatory? Can be changed after installation? | Default Value (evaluated) | Description | Notes
--- | --- | --- | --- | ---
content_origin | Mandatory <br> Changeable | | A URL consisting of the protocol and domain/ip/port only (e.g., `https://foo.com`) for how to access the Pulp server/cluster. Specifically, this is the URL to the pulp_content host that clients will access, and that will be appended to in HTTP responses by multiple content plugins. Any load balancers / proxies (such as those in the [pulp_webserver](../../roles/pulp_webserver) role) should normally be specified instead of the pulp content host itself. Syntax is `(http\|https)://(hostname\|ip)[:port]`. | If pulp is installed on a single server, a commonly acceptable value is `https://{{ ansible_fqdn }}`.
secret_key | Mandatory <br> Changeable | | In order to get a pulp server up and running a [Django SECRET_KEY](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key) must be provided. | It is recommended to make it 50 random characters long from the character set `abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)`. [Pulp docs](https://docs.pulpproject.org/pulpcore/configuration/settings.html?highlight=secret_key#secret-key) have a code snippet to generate it.
`databases.default` | Changeable | (See nested variables listed immediately below) | A dictionary. Its primary use is by this role, where it configures Pulp on how to talk to the database via a larger set of settings. Its secondary use is by the [pulp_database](../../roles/pulp_database) role, where it configures the database server according to a smaller set of settings. The larger set of settings is listed in the [Django Docs](https://docs.pulpproject.org/pulpcore/configuration/settings.html). The settings that are defaulted to are listed below. See [pulpcore docs](https://docs.pulpproject.org/pulpcore/installation/instructions.html#user-and-database-configuration) for more info. | These default settings are merged by the installer with your own; merely setting databases.default with 1 setting under it will not blow away all the other default settings. |
`databases.default.HOST` | Changeable | localhost | The hostname or IP address of the Postgres database server (or cluster) to talk to. | Change this if [pulp_database](../../roles/pulp_database) was applied to a different host, or if accessing an existing postgres server/cluster.
`databases.default.ENGINE` | Changeable | `django.db.backends.postgresql` | The database engine to use. | Do not change it (there is currently no alternative for talking to PostgreSQL, and Pulp only supports PostgreSQL.)
`databases.default.NAME` | Changeable | pulp | The name of the Pulp database to access.
`databases.default.USER` | Changeable | pulp | The user account to authenticate as to access the database.
`databases.default.PASSWORD` | Changeable | pulp | The user account's password for accessing the database.| Please change it to something secure!
cache_enabled | Changeable | true | Whether or not to connect to a redis server to use as a cache.
redis_host | Changeable | localhost | Hostname or IP of the redis server to connect to.
redis_port | Changeable | 6379 | TCP port of the redis server to connect to.
redis_db | Changeable | |The name of the redis database to connect to.
redis_password | Changeable | |  Password for connecting to redis.
redis_url | Changeable | |Tells pulp how to connect to redis. If set, the pulp application overrides individual pulp `pulp_settings.redis_` settings on how to connect, such as `pulp_settings.redis_host` and `pulp_settings.redis_port`. If it is a path to a UNIX domain socket, the pulp_common role will add the `{{ pulp_user }}` user to the `redis` group, if that group exists. Thus giving pulp access to the redis UNIX domain socket. | Make sure to set the same value as you set for `pulp_redis_bind`, as documented in [pulp_redis](../../roles/pulp_redis). Recommended value for a UNIX domain socket is: `unix:/var/run/redis/redis.sock`)
content_path_prefix | Changeable | /pulp/content | The URL under which the content will be served. | Make sure to append the trailing slash.
static_url | | /assets/ | The subdirectory portion of the URL (e.g., "bar" in "http://foo/bar") under which static content is served by the pulp_api service. | See `pulp_settings.static_root`, this is a component of its default value. Can be changed after installation, but you must set `pulp_settings.static_root` back to its original evaluated value.
db_encryption_key| | `{{ pulp_certs_dir }}/database_fields.symmetric.key` (`/etc/pulp/certs/database_fields.symmetric.key`) | Location on disk for the [database fields encryption key](https://docs.pulpproject.org/pulpcore/configuration/settings.html?highlight=encryption#db-encryption-key) | The installer generates this key file by default. See `pulp_db_fields_key` under the [pulp_database_config](../../roles/pulp_database_config) role for how to import a key file instead.
deploy_root | | `{{ pulp_user_home }}` <br> ( /var/lib/pulp ) |  Location on disk where `pulp_settings.static_root`, `pulp_settings.working_directory` and `pulp_settings.media_root` are stored in subdirectories under. | Can be changed after installation but you must change all 3 variables back to their original evaluated values.
file_upload_temp_dir | | `{{ pulp_settings.working_directory }}` <br> ( /var/lib/pulp/tmp ) | The directory to store data to (typically files larger than pulp_settings.[file_upload_max_memory_size](https://docs.djangoproject.com/en/4.0/ref/settings/#file-upload-max-memory-size)) temporarily while uploading files | This setting actually comes from [Django](https://docs.djangoproject.com/en/4.0/ref/settings/#file-upload-temp-dir) rather than from Pulp.
media_root | | `{{ pulp_settings.deploy_root }}/media` <br> ( /var/lib/pulp/media ) |  Location where Pulp will store files (the content that is served.)
static_root | | `{{ pulp_user_home }}{{ pulp_settings.static_url }}` <br> ( /var/lib/pulp/assets/ ) |  Location on disk of the static content served by the pulpcore-api service.
working_directory | | `{{ pulp_settings.deploy_root }}/tmp` <br> ( /var/lib/pulp/tmp ) | Location of Pulp cache.

* **Example**:

    ```yaml
        pulp_settings:
          content_origin: "https://{{ ansible_fqdn }}"
          secret_key: secret
          databases:
            default:
              HOST: postgres-server
              NAME: pulp
              USER: pulp
              PASSWORD: password
          redis_host: redis-server
    ```

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
      pulp-zero: # Effectively python3-pulp-zero
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
* `pulp_pkg_selinux_name`: The name of the package containing the SELinux policies to install. See
  `pulp_install_selinux_policies`, except `git` is not used; the package manager is used instead.
   Defaults to "pulpcore-selinux".

Role Variables for advanced usage
---------------------------------

* `pulpcore_version`: Specify a minor version of pulpcore (e.g.: `3.15`) one would like to install or upgrade to.
   By default the installer will do the right thing by using the minor version of pulpcore it is designed
   for and tested with. This can also be a specific patch release (e.g.: `3.15.2`).
* `pulp_service_timeout`: Set timeout value for pulp services. Defaults to 90.
* `galaxy_lock_requirements`: If set to 0, when installing the plugin `galaxy-ng` from a source
  directory (e.g., cloned via git), unlock the version requirements (i.e., install the latest versions)
  of its dependency plugins, which are listed in `galaxy_dev_source_path`. If set to `1`, the version
  constraints that galaxy-ng has for them are preserved. Defaults to `0` if galaxy-ng's `git_revision`
  isn't specified or if it is set to "main". Defaults to `1` if galaxy-ng's `git_revision` is set to
  any other git commitish (e.g., another branch.)
* `galaxy_dev_source_path`: See `galaxy_lock_requirements`. Defaults to
  `pulpcore:pulp_ansible:pulp_container:galaxy_ng:galaxy-importer`.

Shared Variables
----------------

This role always depends on the [`pulp_repos`](../helper_roles/pulp_repos) role. This is not a static dependency, but a dynamic depenedency at runtime which always occurs. Note that pulp_repos has a global
variable `pulp_repos_enable`, which can be set to `False` to effectively disable the entire `pulp_repos`
role.

This role conditionally (and dynamically) depends on the [`pulp_rpm_prerequisites`](../helper_roles/pulp_rpm_prerequisites) role, whenever `pulp-rpm` is in [`pulp_install_plugins`](#role-variables).

This role conditionally (and dynamically) depends on the [`galaxy_post_install`](../helper_roles/galaxy_post_install) role, whenever `pulp-rpm` is in [`pulp_install_plugins`](#role-variables).

* `prereq_pip_packages`: A List of additional pip packages to install in the virtual
  environment before installing pulp or its content plugins.
  Defaults to a list containing the single item "Jinja2" (which is necessary for pulp_installer to
function). Also, a `prereq_role` may append to it.

* `pulp_settings.databases.default`: Documented above in the [`pulp_settings`](#pulp_settings-variables) table as `databases.default`. This variable is shared with the [pulp_database](../../roles/pulp_database) role.

Several other variables are shared with the [pulp_webserver](../roles/pulp_webserver) role as well. Consult its documentation for more info.

Operating System Variables
--------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

Idempotency
-----------

This role is idempotent by default. Idempotency is dependent on these settings remaining `false`:

* Every `upgrade` under `pulp_install_plugins`
* pulp_upgraded_manually

License
-------

GPLv2+

Author Information
------------------

Pulp Team

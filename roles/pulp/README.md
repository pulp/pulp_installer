Pulp
====

Ansible role that installs Pulp 3 from PyPi or source and provides basic config.

The default administrative user for the Pulp application is: 'admin'

Role Variables
--------------
* `pulp_install_plugins`: A nested dictionary of plugin configuration options.
  Defaults to "{}", which will not install any plugins.
    * *Dictionary Key*: The pip installable plugin name. This is defined in each plugin's `setup.py`. **Required**.
    * `version`: Specific release of the plugin to install from PyPI. If `source_dir` is set, this has no effect. Note that if the specified release of the plugin is incompatible with pulpcore's version, pulp_installer will fail (and exit the play) when it goes to install or upgrade the plugin. Defaults to nothing.
    * `version` and `upgrade` **cannot be used together**. Even though a command like `pip install --upgrade pulp-file=0.3.0` is valid, the ansible pip module refuses to let you specify version and `state=latest` (`state=latest` maps to `pip --upgrade`, and to our upgrade: true).
    * `upgrade`: Whether to update/upgrade the plugin to the latest stable release from PyPI. Only affects systems where the plugin is already installed. If `source_dir` is set, this has no effect and is effectively always `true`. Mutually exclusive with `version`. Note that if the latest stable release of the plugin is incompatible with pulpcore's version, pulp_installer will fail (and exit the play) when it goes to upgrade the plugin. Defaults to "false".
    * `source_dir`: Optional. Absolute path to the plugin source code. If present,
  plugin will be installed from source in editable mode.
  Also accepts a pip VCS URL, to (for example) install the master branch.
    * `prereq_role`: Optional. Name of (or folder path to) Ansible role to run
    immediately before the venv is created. You will need to download it 1st (with
    ansible-galaxy.) Needed because many plugins will have OS dependencies in C.
    See `prereq_pip_packages` also.
    * **Example**:
    ```yaml
    pulp_install_plugins:
      pulp-zero: {}
      pulp-one: # plugin name (pulp-ansible, pulp-container, pulp-rpm, ...)
        version: "1.0.1" # specific release (pulp-file-0.3.0)
      pulp-two:
        upgrade: true # upgrade to the latest stable release from PyPI
      pulp-three:
        source_dir: "/var/lib/pulp/pulp_three" # path to the plugin source code
      pulp-four:
        prereq_role: "pulp.pulp_three_role" # role to run immediately before the venv is created
    ```
* `pulp_cache_dir`: Location of Pulp cache. Defaults to "/var/lib/pulp/tmp".
* `pulp_config_dir`: Directory which will contain Pulp configuration files.
  Defaults to "/etc/pulp".
* `pulp_default_admin_password`: Initial password for the Pulp admin. **Required**.
* `pulp_install_dir`: Location of a virtual environment for Pulp and its Python
  dependencies. Defaults to "/usr/local/lib/pulp".
* `pulp_user_home`: equivalent to `MEDIA_ROOT` from `pulpcore` i.e. absolute path for pulp user home.
* `pulp_install_api_service`: Whether to create systemd service files for
  pulpcore-api. Defaults to "true".
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
* `pulp_api_bind` Interface and Port where Pulp Content `gunicorn` service will listen. Defaults to
  '127.0.0.1:24817'. This variable is the value used to render the `pulpcore-api.service.j2` template
  passing to the `--bind` parameter of the `gunicorn` service.
* `pulp_api_workers`: Number of Pulp Content `gunicorn` processes for handling requests. Defaults to 1.
  Used to render the `pulpcore-api.servie.j2` template, passing to the `--workers` parameter of the
  gunicorn service.
* `pulp_settings`: A nested dictionary that is used to add custom values to the user's
    `setting.py`, which will override any default values set by pulpcore. The keys of this
    dictionary are variable names, and the values should be expressed using the [Dynaconf syntax](
    https://dynaconf.readthedocs.io/en/latest/guides/environment_variables.html#precedence-and-type-casting)
    Please see [pulpcore configuration
    docs](https://docs.pulpproject.org/en/3.0/nightly/installation/configuration.html#id2) for
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

License
-------

GPLv2+

Author Information
------------------

Pulp Team

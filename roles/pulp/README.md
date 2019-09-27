Pulp
====

Ansible role that installs Pulp 3 from PyPi or source and provides basic config.

The default administrative user for the Pulp application is: 'admin'

Role Variables:
---------------

* `pulp_cache_dir`: Location of Pulp cache. Defaults to "/var/lib/pulp/tmp".
* `pulp_config_dir`: Directory which will contain Pulp configuration files.
  Defaults to "/etc/pulp".
* `pulp_default_admin_password`: Initial password for the Pulp admin. **Required**.
* `pulp_install_dir`: Location of a virtual environment for Pulp and its Python
  dependencies. Defaults to "/usr/local/lib/pulp".
* `prereq_pip_packages`: Additional pip packages to install in the virtual
  environment before installing pulp or its content plugins.
  Defaults to an empty list, but plugin prerequisite roles may append to it.
* `pulp_install_plugins`: A nested dictionary of plugin configuration options.
  Defaults to "{}", which will not install any plugins.
  * Dictionary Key: The pip installable plugin name. This is defined in each
  plugin's* `setup.py`. **Required**.
  * `source_dir`: Optional. Absolute path to the plugin source code. If present,
  plugin will be installed from source in editable mode.
* `pulp_install_api_service`: Whether to create systemd service files for
  pulp-api. Defaults to "true".
* `pulp_source_dir`: Optional. Absolute path to Pulp source code. If present, Pulp
  will be installed from source in editable mode.
* `pulp_user`: User that owns and runs Pulp. Defaults to "pulp".
* `pulp_user_id`: Integer value of uid for the `pulp_user`. Defaults to nothing and uid is assigned
  by the system.
* `pulp_group`: The group that the `pulp_user` belongs to. Defaults to `pulp`.
* `pulp_group_id`: Integer value of gid for the `pulp_group`. Defaults to nothing and gid is
  assigned by the system.
* `pulp_use_system_wide_pkgs` Use python system-wide packages. Defaults to "false".
* `pulp_remote_user_environ_name` Optional. Set the `REMOTE_USER_ENVIRON_NAME` setting for Pulp.
  This variable will be set as the value of `CONTENT_HOST` as the base path to build content URLs.
* `pulp_api_bind` Interface and Port where Pulp Content `gunicorn` service will listen. Defaults to
  '127.0.0.1:24817'. This variable is the value used to render the `pulp-api.service.j2` template
  passing to the `--bind` parameter of the `gunicorn` service.
* `pulp_settings`: A nested dictionary that is used to add custom values to the user's
    `setting.py`, which will override any default values set by pulpcore. The keys of this
    dictionary are variable names, and the values can be nested. Please see [pulpcore configuration
    docs](https://docs.pulpproject.org/en/3.0/nightly/installation/configuration.html#id2) for
    documentation on the possible values.
  * `pulp_settings.secret_key`: **Required**. Pulp's Django application `SECRET_KEY`.


Shared Variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role is required by the `pulp-database` role and uses some variables from it.

* `pulp_settings_db_defaults`: See pulp-database README.


Operating System Variables:
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

License
-------

GPLv2

Author Information
------------------

Pulp Team

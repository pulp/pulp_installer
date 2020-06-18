pulp_api
=========

Install, configure, and set the state of the pulp API service.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

* `pulp_api_bind` Interface and Port where Pulp Content `gunicorn` service will listen. Defaults to
  '127.0.0.1:24817'. This variable is the value used to render the `pulpcore-api.service.j2` template
  passing to the `--bind` parameter of the `gunicorn` service.
* `pulp_api_workers`: Number of Pulp Content `gunicorn` processes for handling requests. Defaults to 1.
  Used to render the `pulpcore-api.service.j2` template, passing to the `--workers` parameter of the
  gunicorn service.

Shared variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** to the required `pulp_common` role, and inherits
some of its variables.

* `pulp_config_dir`
* `pulp_install_dir`
* `pulp_ld_library_path`: An optional LD_LIBRARY_PATH environment variable for the pulpcore-api systemd process
* `pulp_settings_file`
* `pulp_user`

pulp_content
============

Install, configure, and set the state of pulp content app.

Role Variables
--------------

* `pulp_content_bind`: Interface and Port where Pulp Content [`gunicorn` service will
  listen.](https://docs.gunicorn.org/en/stable/settings.html#bind)

One can specify a unix socket path instead
(recommended value is `'unix:/var/run/pulpcore-content/pulpcore-content.sock'`).

Defaults to `'127.0.0.1:24816'`.

Shared variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** to the required `pulp_common` role, and inherits
some of its variables.

* `pulp_config_dir`
* `pulp_group`
* `pulp_install_dir`
* `pulp_ld_library_path`: An optional LD_LIBRARY_PATH environment variable for the pulpcore-api systemd process
* `pulp_settings_file`
* `pulp_user`

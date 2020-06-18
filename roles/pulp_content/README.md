pulp_content
=============

Install, configure, and set the state of pulp content app.

Variables
---------

* `pulp_content_bind`: Interface and Port where Pulp Content `gunicorn` service will listen.

This variable is the value used to render the `pulpcore-content.service.j2` template passing
to the `--bind` parameter of the gunicorn service.

Defaults to `127.0.0.1:24816`

Shared variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** to the required `pulp_common` role, and inherits
some of its variables.

* `pulp_user`
* `pulp_install_dir`
* `pulp_config_dir`
* `pulp_settings_file`
* `pulp_ld_library_path`: An optional LD_LIBRARY_PATH environment variable for the pulpcore-content systemd process

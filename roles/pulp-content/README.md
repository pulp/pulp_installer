pulp-content
=============

Install, configure, and set the state of pulp content app.

Variables:
----------

* `pulp_content_host`: Host and port where Pulp content app is served. Defaults to `localhost:8080`

This variable will be set as the value of `CONTENT_HOST` config in `{{pulp_config_dir}}/settings.py` as the base path to build content URLs and also is the value passed to the `--bind` parameter of the `pulpcore.content` gunicorn service.

Shared variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is not tightly coupled** with the `pulp` role, but it does use some of the same
variables. When used together, the values are inherited from the role. When not used together,
these values are **required**.

* `pulp_user`
* `pulp_install_dir`

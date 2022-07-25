pulp_content
============

Install, configure, and set the state of pulp content app.

This role depends on the [pulp_common](../../roles/pulp_common) role, see it for many more variables on configuring pulp_content.

Role Variables
--------------

* `pulp_content_bind`: Interface and Port where Pulp Content [`gunicorn` service will
  listen.](https://docs.gunicorn.org/en/stable/settings.html#bind)
* `pulp_content_workers`: Number of `gunicorn` processes for handling Pulp content app requests.
  Defaults to 8.

One can specify a unix socket path instead
(recommended value is `'unix:/var/run/pulpcore-content/pulpcore-content.sock'`).

Defaults to `'127.0.0.1:24816'`.

Shared variables
----------------

This role depends upon the the [`pulp_common`](../helper_roles/pulp_common) role, which in turn depends on on [pulp_repos](../helper_roles/pulp_repos). You should consult [`pulp_common`](../helper_roles/pulp_common) in particular for variables that effectively control the behavior of this role.

This role also utilizes some of the pulp_common role's variables in its logic:

* `pulp_config_dir`
* `pulp_group`
* `pulp_install_dir`
* `pulp_ld_library_path`: An optional LD_LIBRARY_PATH environment variable for the pulpcore-api systemd process
* `pulp_settings_file`
* `pulp_user`

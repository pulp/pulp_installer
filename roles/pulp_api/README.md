pulp_api
========

Install, configure, and set the state of the pulp API service.

Role Variables
--------------

* `pulp_api_bind`: Interface and Port where Pulp Content [`gunicorn` service will
  listen.](https://docs.gunicorn.org/en/stable/settings.html#bind)
  One can specify a unix socket path instead (recommended value is `'unix:/var/run/pulpcore-api/pulpcore-api.sock'`).
  Defaults to `'127.0.0.1:24817'`.
* `pulp_api_workers`: Number of `gunicorn` processes for handling Pulp API requests. Defaults to 1.
* `pulp_token_auth_key`: Location of the openssl private key (in pem format) to use for token
  authentication. If not specified, a new key wil be generated. (Only generated if one doesn't
  exist.)

Shared variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** to the required `pulp_common` role, and inherits
some of its variables.

* `pulp_certs_dir`: Path where to generate or drop the key for authentication token. Defaults to
  '{{ pulp_config_dir }}/certs' .
* `pulp_config_dir`
* `pulp_group`
* `pulp_install_dir`
* `pulp_ld_library_path`: An optional LD_LIBRARY_PATH environment variable for the pulpcore-api systemd process
* `pulp_settings_file`
* `pulp_user`

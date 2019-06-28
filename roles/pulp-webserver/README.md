pulp-webserver
==============

Install, configure, start, and enable a web server.

Currently, Nginx and Apache are supported. They are configured as a reverse proxy to the pulp-api
and pulp-content-app Gunicorn processes.


Variables:
----------

* `pulp_content_port` Set the port the reverse proxy should connect to for the Content app. Defaults
  to '24816'.
* `pulp_content_host` Set the host the reverse proxy should connect to for the Content app. Defaults
  to '127.0.0.1'.
* `pulp_api_port` Set the port the reverse proxy should connect to for the API server. Defaults to
  '24817'.
* `pulp_api_host` Set the host the reverse proxy should connect to for the API server. Defaults to
  '127.0.0.1'.


Shared variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role is **not tightly coupled** to the `pulp` role, but uses some of the same
variables. When used in the same play, the values are inherited from the `pulp`
role.

* `pulp_install_dir`: Location of a virtual environment for Pulp and its Python
  dependencies. **Required** if used in a separate play from the `pulp` role. Value
  must match the value used in the `pulp` role.

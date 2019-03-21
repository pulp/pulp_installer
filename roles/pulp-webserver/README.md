pulp-webserver
===============

Install, configure, start, and enable a web server.

Currently, the only web server that this role can install is Nginx. In the
future, additional web servers such as Apache or LightTPD might be supported.

Shared variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role is **not tightly coupled** to the `pulp` role, but uses some of the same
variables. When used in the same play, the values are inherited from the `pulp`
role.

* `pulp_install_dir`: Location of a virtual environment for Pulp and its Python
  dependencies. **Required** if used in a separate play from the `pulp` role. Value
  must match the value used in the `pulp` role.

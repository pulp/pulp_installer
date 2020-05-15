pulp_redis
==========

Install and start Redis, and install RQ in the Pulp virtualenv.

Shared Variables:
-----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role is **not tightly coupled** to the `pulp` role, but uses some of the same
variables. When used in the same play, the values are inherited from the `pulp`
role. When not used together, this role provides identical defaults.

* `pulp_user`: User that owns and runs Redis. Defaults to "pulp".
* `pulp_install_dir`: Location of a virtual environment for Redis and its Python
  dependencies. Defaults to "/usr/local/lib/pulp".


Operating Systems Variables:
----------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

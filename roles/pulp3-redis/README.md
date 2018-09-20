pulp3-redis
===========

Install and start redis, and install RQ in the Pulp virtualenv.

Shared Variables:
-----------------

This role is **not tightly coupled** to the `pulp3` role, but uses some of the same
variables. When used in the same play, the values are inherited from the `pulp3`
role. When not used together, this role provides identical defaults.

* `pulp_user`: User that owns and runs redis. Defaults to "pulp".
* `pulp_install_dir`: Location of a virtual environment for redis and its Python
  dependencies. Defaults to "/usr/local/lib/pulp".


Operating Systems Variables:
----------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

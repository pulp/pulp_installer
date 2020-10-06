pulp_redis
==========

Install and start Redis.

Role Variables
--------------

* `pulp_redis_bind`: Interface and Port where Redis service will listen. One can specify a unix
   socket path instead (recommended value is `'unix:/var/run/redis/redis.sock'`). Defaults to `'127.0.0.1:6379'`.
* `pulp_redis_package_name`: Name of the redis package server to install. Defaults to: `redis`
* `pulp_redis_server_name`: Name of the redis server service to run. Defaults to: OS specific
* `pulp_redis_conf_file`: Path to the redis server configuration file. Defaults to: os specific

Shared Variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role is **not tightly coupled** to the `pulp_common` role, but uses some of the same
variables. When used in the same play, the values are inherited from the role.
When not used together, this role provides identical defaults.

* `pulp_user`: User that owns and runs Redis. Defaults to "pulp".

Operating Systems Variables
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

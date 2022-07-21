pulp_redis
==========

Install, Configure and start Redis.

Role Variables
--------------

* `pulp_cache_enabled`: Install and enable Redis as a cache. Defaults to `True`
  This option effectively disables or enables this entire role.
* `pulp_redis_bind`: Interface and Port where Redis service will listen. One can specify a unix
   socket path instead (recommended value is `'unix:/var/run/redis/redis.sock'`). Defaults to `'127.0.0.1:6379'`.
* `pulp_redis_package_name`: Name of the redis package server to install. Defaults to: `redis`
* `pulp_redis_server_name`: Name of the redis server service to run. Defaults to: OS specific
* `pulp_redis_conf_file`: Path to the redis server configuration file. Defaults to: os specific

Shared Variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role is **not tightly coupled** to the [pulp_common](../../roles/pulp_common) role, but uses some of the same
variables.

* `pulp_user`: OS user account that accesses the redis database, potentially over a UNIX socket. Defaults to "pulp". NOTE: Technically, this variable is used by the pulp_common role rather than the pulp_redis role. If pulp_common detects that the pulp_redis role has been run against a pulp host (or more broadly, if the `redis` group exists on the system), the pulp user will be added to the `redis` group. This enables the UNIX socket access to redis.

Operating Systems Variables
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

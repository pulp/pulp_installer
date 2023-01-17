pulp_redis
==========

Install, Configure and start Redis.

Role Variables
--------------

* `pulp_cache_enabled`: Install and enable Redis as a cache. Defaults to `True`
  This option effectively disables or enables this entire role.
* `pulp_redis_bind`: Interface and Port where Redis service will listen. One can specify a unix
   socket path instead (recommended value is `'unix://var/run/redis/redis.sock'`). Defaults to `'127.0.0.1:6379'`.
* `pulp_redis_package_name`: Name of the redis package server to install. Defaults to: `redis`
* `pulp_redis_server_name`: Name of the redis server service to run. Defaults to: OS specific
* `pulp_redis_conf_file`: Path to the redis server configuration file. Defaults to: os specific

Shared Variables
----------------

This role depends upon the the [pulp_repos](../helper_roles/pulp_repos) role in order to enable the EPEL repo.
Its variables effectively control the behavior of this role.

Operating Systems Variables
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

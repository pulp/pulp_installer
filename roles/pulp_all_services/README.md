pulp_all_services
=================

A role to install all Pulp 3 services ([first-party](#first-party-services) &
[third-party](#third-party-services)) on a single host.

Users are supposed to specify this role as a single stable role name
in their playbooks, rather than every single service role name, which
are subject to change. The exception is when they want certain services
on certain hosts.

Currently, all it does is depend on the required roles, which are
subject to change over time. They are specified in the following order:

- [pulp_database](../../roles/pulp_database)
- [pulp_redis](../../roles/pulp_redis)
- [pulp_services](../pulp_services)
- [pulp_database_config](../../roles/pulp_database_config) (implicitly via pulp_services)
- [pulp_api](../../roles/pulp_api) (implicitly via pulp_services)
- [pulp_content](../../roles/pulp_content) (implicitly via pulp_services)
- [pulp_workers](../../roles/pulp_workers) (implicitly via pulp_services)
- [pulp_common](../../roles/pulp_common) (implicitly via pulp_services)
- [pulp_health_check](../../roles/pulp_health_check)
- [pulp_webserver](../../roles/pulp_webserver)

Related Roles
-------------

- [pulp_services](../pulp_services/): A role to install & configure Pulp 3's
  first-party services (including the state of the Pulp database) on a single host.

Definitions
-----------

### First-Party Services

The first-party services are services written by the Pulp project itself.

### Third-Party Services

The third-party services are services written by other open source projects, but
Pulp depends on them as the middle tier in 3-tier application architecture to
run.

The 2 backends are the PostgreSQL database server and the redis server.

The 1 frontend is the Nginx or Apache webserver, with special config to combine
multiple Pulp services into one.

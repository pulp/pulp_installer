pulp_all_services
=================

A role to install all Pulp services on a single host.

Users are supposed to specify this role as a single stable role name
in their playbooks, rather than every single service role name, which
are subject to change. The exception is when they want certain services
on certain hosts.

Currently, all it does is depend on the required roles, which are
subject to change over time:
  - pulp_database
  - pulp_redis
  - pulp_api
  - pulp_content
  - pulp_resource_manager
  - pulp_workers
  - pulp_webserver
  - pulp_common (implicitly)

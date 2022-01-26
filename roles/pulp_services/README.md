pulp_services
=============

A role to install & configure Pulp 3's [first-party services](#first-party-services)
(including the state of the Pulp database) on a single host. [1]

Does not include [third-party services](#third-party-services), which is
significant because Pulp 3 requires special config for 1 of them, the webserver,
to combine multiple Pulp services into one.

Users are supposed to specify this role as a single stable role name
in their playbooks, rather than every single service role name, which
are subject to change. The exception is when they want certain services
on certain hosts.

Currently, all it does is depend on the required roles, which are
subject to change over time:

  - pulp_database_config
  - pulp_api
  - pulp_content
  - pulp_resource_manager
  - pulp_workers
  - pulp_common (implicitly)

Example Usage
-------------

1. Install your own PostgreSQL server.
1. Install your own Redis server.
1. Run the example playbook below against a Pulp host.
1. Install your own webserver (nginx or apache). Consult the pulp_webserver role for
   the necessary config that is not plugin specific.
1. On the Pulp host, check if any plugins have webserver snippets, like in the command seen below.
1. Copy over & install any webserver snippets to the webserver.

Here is an example command & output for checking if any plugins have any webserver snippets.
```
$ ls /usr/local/lib/pulp/lib/python*/site-packages/pulp_*/app/webserver_snippets/{apache.conf,nginx.conf}
/usr/local/lib/pulp/lib/python3.6/site-packages/pulp_container/app/webserver_snippets/apache.conf
/usr/local/lib/pulp/lib/python3.6/site-packages/pulp_container/app/webserver_snippets/nginx.conf
```

Here's an example playbook for using pulp_services in pulp_installer. It assumes the database, redis & webserver are on a separate hosts, `redis1`, `postgres1` & `webserver1`. The database and redis must already be up & running.

    ---
    - hosts: all
      vars:
        pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
        pulp_settings:
          secret_key: << YOUR SECRET HERE >>
          content_origin: "https://webserver1.fqdn"
          redis_host: redis1
          redis_port: 6380
          redis_password: << YOUR REDIS PASSWORD HERE >>
          databases:
            default:
              HOST: postgres1
              ENGINE: django.db.backends.postgresql
              NAME: pulp
              USER: pulp
              PASSWORD: << YOUR DATABASE PASSWORD HERE >>
        pulp_install_plugins:
          pulp-rpm: {} #no need to set subvar prereq_role for pulp_rpm specifically
      roles:
        - pulp_services
      environment:
        DJANGO_SETTINGS_MODULE: pulpcore.app.settings

Related Roles
-------------
- [pulp_all_services](../pulp_all_services/): A role to install all Pulp 3
services (first-party & third-party) on a single host.

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

Clustering
==========

In this section, you can find information and Ansible playbook examples that demonstrate how to
configure the following cluster deployment scenarios:

* [A single “all-in-one” Pulp server that includes the database, redis, and webserver.](#all-in-one-pulp-server-example)
* [Pulp on one server, while using existing servers for the database & redis.](#pulp-server-with-existing-infrastructure)
* [Pulp on one server, with the database, redis & webserver on separate servers.](#pulp-with-separate-servers-for-services)
* [Pulp Servers with load-balanced DNS.](#pulp-servers-with-load-balanced-dns)
* [Each and every Pulp service on separate servers.](#separate-servers-for-each-and-every-service)
* [Completely Highly Available Pulp.](#completely-highly-available-pulp)

Depending on your requirements for high availability and better scalability, you might like to
customize your installations according to these examples.

### 'All in One Pulp Server' Example

This deployment consists of installing a single server that contains all Pulp services, including
the database, redis & webserver.

In other words, this is not a cluster, but the simplest possible deployment of Pulp, for comparison
purposes.

```yaml
---
- hosts: example-pulp-server
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://{{ ansible_facts.fqdn }}"
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  roles:
    - pulp_all_services
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```

### Pulp Server with Existing Infrastructure

This deployment consists of a single Pulp server that relies on the following services being
existing and external. No new servers are used or created for them:

* Database (`example-existing-postgres-server`)
* Redis (`example-existing-redis-server`)s

```yaml
---
- hosts: example-pulp-server
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://{{ ansible_facts.fqdn }}"
      redis_host: example-existing-redis-server
      redis_port: 6379
      redis_password: << YOUR REDIS PASSWORD HERE >>
      databases:
        default:
          HOST: example-existing-postgres-server
          PORT: 5432
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  roles:
    - pulp_services
    - pulp_health_check
    - pulp_webserver
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```

### Pulp with Separate Servers for Services

This scenario has the following layout:

* Pulp on one server
* The database on a second server
* redis on a third server
* The webserver on a fourth server

```yaml
---
- hosts: example-postgres-server
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_settings:
      databases:
        default:
          HOST: example-postgres-server
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
  roles:
    - pulp_database

- hosts: example-redis-server
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_redis_bind: 'example-redis-server:6379'
  roles:
    - pulp_redis

- hosts: example-pulp-server
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_api_bind: example-pulp-server:24817
    pulp_content_bind: example-pulp-server:24816
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-webserver.fqdn"
      redis_host: example-redis-server
      databases:
        default:
          HOST: example-postgres-server
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  roles:
    - pulp_services
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts: example-webserver
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_api_bind: example-pulp-server:24817
    pulp_content_bind: example-pulp-server:24816
  roles:
    - pulp_webserver
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```

### Pulp Servers with load-balanced DNS

In this deployment, Pulp (including the webserver) is load balanced to 2 servers, and thus is more
performant, but is not highly available.

The separate server for the database and redis also increases performance.

This relies on a round-robin DNS record that points to all 2 Pulp servers:

* `example-pulp-load-balanced-hostname.fqdn`

This also relies on shared storage (such as NFS) being hosted at the following address:

* `example-nfs-server:/var/lib/pulp`

Adjust the pre_task `Mount /var/lib/pulp` as needed for your shared storage.

This deployment can be scaled up by adding more pulp servers.

Scaling up is performed by:

* Adjusting `- hosts:` to include the new servers (such as `example-pulp-server3`)
* Re-running the installer
* Adjusting the DNS record to add them.

```yaml
---
- hosts: example-postgres-redis-server
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_redis_bind: 'example-redis-server:6379'
    pulp_settings:
      databases:
        default:
          HOST: example-postgres-server
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
  roles:
    - pulp_database
    - pulp_redis

- hosts:
    - example-pulp-server1
    - example-pulp-server2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-pulp-load-balanced-hostname.fqdn"
      redis_host: example-postgres-redis-server
      databases:
        default:
          HOST: example-existing-postgres-server
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  pre_tasks:
    - name: Mount /var/lib/pulp
      mount:
        src: example-nfs-server:/var/lib/pulp
        path: /var/lib/pulp
        opts: rw
        state: mounted
        fstype: nfs
        backup: yes
  roles:
    - pulp_services
    - pulp_health_check
    - pulp_webserver
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```

### Separate Servers for Each and Every service

In this deployment, every single service is deployed on its own server, or on 2 servers.

There are two servers for each of the following services. This means they are highly available:

* Pulp API
* Pulp Content
* Pulp Workers

There is only 1 server for each of the following services. This means they are not highly available:

* Database
* Redis
* Webserver

The installer cannot provide high availability for database or redis. It cannot provide high
availability for the webserver either, that would rely on a highly available load balancer.

The webserver does however make the API and Content be highly available by performing
highly-available load-balancing to them.

This also relies on shared storage (such as NFS) being hosted at the following address:

* `example-nfs-server:/var/lib/pulp`

Adjust the 3 pre_tasks `Mount /var/lib/pulp` as needed for your shared storage.

This deployment can be scaled up by adding more Pulp API, Pulp Content or Pulp Worker servers.

Scaling up is performed by:

* Adjusting `- hosts:` to include the new servers (such as `example-pulp-content-server3`)
* Adjusting `pulp_webserver_api_hosts` and `pulp_webserver_content_hosts` to include the new API or
  content servers
* Re-running the installer

```yaml
---
- hosts: example-postgres-server
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_settings:
      databases:
        default:
          HOST: example-postgres-server
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
  roles:
    - pulp_database

- hosts: example-redis-server
  force_handlers: True
  vars:
    pulp_redis_bind: 'example-redis-server:6379'
  roles:
    - pulp_redis

- hosts:
    - example-pulp-api-server1
    - example-pulp-api-server2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_api_bind: "0.0.0.0:24817"
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-webserver.fqdn"
      redis_host: example-redis-server
      databases:
        default:
          HOST: example-postgres-server
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  pre_tasks:
    - name: Mount /var/lib/pulp
      mount:
        src: example-nfs-server:/var/lib/pulp
        path: /var/lib/pulp
        opts: rw
        state: mounted
        fstype: nfs
        backup: yes
  roles:
    - pulp_api
    - pulp_database_config
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts:
    - example-pulp-content-server1
    - example-pulp-content-server2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_content_bind: "0.0.0.0:24816"
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-webserver.fqdn"
      redis_host: example-redis-server
      databases:
        default:
          HOST: example-postgres-server
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  pre_tasks:
    - name: Mount /var/lib/pulp
      mount:
        src: example-nfs-server:/var/lib/pulp
        path: /var/lib/pulp
        opts: rw
        state: mounted
        fstype: nfs
        backup: yes
  roles:
    - pulp_content
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts:
    - example-pulp-worker-server1
    - example-pulp-worker-server2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-webserver.fqdn"
      redis_host: example-redis-server
      databases:
        default:
          HOST: example-postgres-server
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  pre_tasks:
    - name: Mount /var/lib/pulp
      mount:
        src: example-nfs-server:/var/lib/pulp
        path: /var/lib/pulp
        opts: rw
        state: mounted
        fstype: nfs
        backup: yes
  roles:
    - pulp_workers
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts:
    - example-pulp-api-server1
    - example-pulp-api-server2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  roles:
    - pulp_health_check
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts: example-webserver
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_webserver_api_hosts:
      - address: example-pulp-api-server1:24817
      - address: example-pulp-api-server2:24817
    pulp_webserver_content_hosts:
      - address: example-pulp-content-server1:24816
      - address: example-pulp-content-server2:24816
  roles:
    - pulp_webserver
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```

Note that one of the 2 API servers will be randomly chosen to actually run the role
`pulp_database_config`.
This server will create and migrate the database for Pulp.

### Completely Highly Available Pulp

In this deployment, every part of the Pulp application stack is highly available.

Any service which pulp_installer cannot make highly available, or cannot deploy at all, is an external
service.

This means that the following services are external, and are already setup in a highly available
manner:

* Load balancer (provides `example-pulp-load-balanced-hostname.fqdn`)
* Database (`example-existing-postgres-cluster`)
* Redis (`example-existing-redis-cluster`)
* Shared storage (such as NFS) (`/var/lib/pulp`)

But the installer will install 2 instances of each of the following:

* Pulp API
* Pulp Content
* Pulp Workers
* Pulp Webserver

This also relies on shared storage (such as NFS) being hosted at the following address:

* `example-nfs-server:/var/lib/pulp`

Adjust the 3 pre_tasks `Mount /var/lib/pulp` as needed for your shared storage.

This deployment can be scaled up by adding more Pulp API, Pulp Content, Pulp Worker or Pulp
Webserver servers.

Scaling up is performed by:

* Adjusting `- hosts:` to include the new servers (such as `example-pulp-content-server3`)
* Adjusting `pulp_webserver_api_hosts` and `pulp_webserver_content_hosts` to include the new API or
  content servers
* Re-running the installer
* Adjusting the load balancer to add the new Pulp Webservers

```yaml
---
- hosts:
    - example-pulp-api-server1
    - example-pulp-api-server2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_api_bind: "0.0.0.0:24817"
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-pulp-load-balanced-hostname.fqdn"
      redis_host: example-existing-redis-cluster
      redis_port: 6379
      redis_password: << YOUR REDIS PASSWORD HERE >>
      databases:
        default:
          HOST: example-existing-postgres-cluster
          PORT: 5432
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  pre_tasks:
    - name: Mount /var/lib/pulp
      mount:
        src: example-nfs-server:/var/lib/pulp
        path: /var/lib/pulp
        opts: rw
        state: mounted
        fstype: nfs
        backup: yes
  roles:
    - pulp_api
    - pulp_database_config
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts:
    - example-pulp-content-server1
    - example-pulp-content-server2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_content_bind: "0.0.0.0:24816"
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-pulp-load-balanced-hostname.fqdn"
      redis_host: example-existing-redis-cluster
      redis_port: 6379
      redis_password: << YOUR REDIS PASSWORD HERE >>
      databases:
        default:
          HOST: example-existing-postgres-cluster
          PORT: 5432
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  pre_tasks:
    - name: Mount /var/lib/pulp
      mount:
        src: example-nfs-server:/var/lib/pulp
        path: /var/lib/pulp
        opts: rw
        state: mounted
        fstype: nfs
        backup: yes
  roles:
    - pulp_content
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts:
    - example-pulp-worker-server1
    - example-pulp-worker-server2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-pulp-load-balanced-hostname.fqdn"
      redis_host: example-existing-redis-cluster
      redis_port: 6379
      redis_password: << YOUR REDIS PASSWORD HERE >>
      databases:
        default:
          HOST: example-existing-postgres-cluster
          PORT: 5432
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container:
      pulp-rpm:
  pre_tasks:
    - name: Mount /var/lib/pulp
      mount:
        src: example-nfs-server:/var/lib/pulp
        path: /var/lib/pulp
        opts: rw
        state: mounted
        fstype: nfs
        backup: yes
  roles:
    - pulp_workers
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts:
    - example-pulp-api-server1
    - example-pulp-api-server2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  roles:
    - pulp_health_check
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts:
    - example-webserver1
    - example-webserver2
  force_handlers: True
  collections:
    - pulp.pulp_installer
  vars:
    pulp_webserver_api_hosts:
      - address: example-pulp-api-server1:24817
      - address: example-pulp-api-server2:24817
    pulp_webserver_content_hosts:
      - address: example-pulp-content-server1:24816
      - address: example-pulp-content-server2:24816
  roles:
    - pulp_webserver
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```

Firewall Configuration
======================

Pulp on a Single Server
-----------------------

If installed on a single server, Pulp only needs the 2 webserver ports open:

Port  | Variable | Purpose
--- | --- | ---
80  |  pulp_webserver_http_port | Redirecting to https
443 | pulp_webserver_https_port | The entire Pulp application

To open these ports with firewalld (default firewall on Fedora, RHEL, CentOS)
```
firewall-cmd --add-service=http
firewall-cmd --permanent --add-service=http
firewall-cmd --add-service=https
firewall-cmd --permanent --add-service=https
```

To open these ports on ufw (default firewall on Ubuntu)
```
ufw allow "Nginx Full"

```

Pulp on a Cluster
-----------------

If each role is installed to a cluster, the host must have open the ports for its role:

Port | Variable | Role | Accessed by | Purpose
--- | --- | --- | --- | ---
80 | `pulp_webserver_http_port` | [pulp_webserver](../../roles/pulp_webserver) | API and content users/clients | Redirecting to https
443 | `pulp_webserver_https_port` | [pulp_webserver](../../roles/pulp_webserver) | API and content users/clients | The entire Pulp application
5432 | See "Purpose" | [pulp_database](../../roles/pulp_database) | pulp_api, pulp_content, pulp_workers | The PostgreSQL database server. It is configured by overrding the variable `postgresql_global_config_options` ( as seen in [pulp_database vars.yml](__pulp_database_remote_postgresql_global_config_options:)) to include an additional array item of a dictionary, with the variable under it "option" set to "port", and the variable "value" set to the port number.
6379 | `pulp_redis_bind` | [pulp_redis](../../roles/pulp_redis) | pulp_api, pulp_content, pulp_workers | Redis cache server
24816 | `pulp_content_bind` | [pulp_content](../../roles/pulp_content) | pulp_webserver |The pulp Content service
24817 | `pulp_api_bind` | [pulp_api](../../roles/pulp_api) | pulp_webserver | The pulp API service

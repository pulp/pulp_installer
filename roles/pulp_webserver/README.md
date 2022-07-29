pulp_webserver
==============

Install, configure, start, and enable a web server.

This webserver acts as a front-end for the Pulp Application, reverse proxying certain URLs to one or
more pulp-api hosts, and other URLs to one or more pulp-content hosts. If there are multiple api or
content hosts, load balancing is performed.

No configuration is mandatory if the the web server is installed on the same host as the pulp-api
and pulp-content servers/roles.

Nginx and Apache are supported as the web server.

By default TLS will be enabled (with self-signed certificates if none are provided). An automatic
redirect from http to https will take place.

Role Variables
--------------

* `pulp_webserver_server` Set the webserver Pulp should use to reverse proxy with. Defaults to
  `nginx`. The other valid value is `apache`.
* `pulp_webserver_http_port`: Define the HTTP port to listen on. Defaults to `80`.
* `pulp_webserver_https_port`: Define the HTTPS port to listen on. Defaults to `443`.
* `pulp_webserver_disable_https`: Whether or not HTTPS should be disabled. Defaults to `false`.
* `pulp_webserver_disable_hsts`: Whether or not HSTS should be disabled. Defaults to `false`.
* `pulp_webserver_tls_cert`: Relative or absolute path to the TLS (SSL) certificate
   one wants to import.
* `pulp_webserver_tls_key`: Relative or absolute path to the TLS (SSL) key
   one wants to import.
* `pulp_webserver_tls_custom_ca_cert` A custom CA certificate to import on the server.
* `pulp_webserver_tls_files_remote`: Whether or not `pulp_webserver_tls_cert`,
  `pulp_webserver_tls_key` & `pulp_webserver_tls_custom_ca_cert` are on the webserver (`true`)
   or on the ansible management node (`false`). Defaults to `false`.
* `pulp_webserver_httpd_servername`: Servername to use when deploying httpd. Defaults to
  `ansible_fqdn`.
* `pulp_webserver_static_dir` absolute path where to place static files, such as for the .well-known
   directory for ACME (letsencrypt) files or SSL certs. This is not to be confused with the Pulp
   application's setting `STATIC_ROOT`, which is a function of Pulp itself (not the webserver) and servces
   a different set of files. Defaults to `{{ pulp_user_home}}/pulpcore_static`, which is `/var/lib/pulp/pulpcore_static`
* `pulp_client_max_body_size`: Sets the maximum allowed size of the client request body.

Role Variables for Clusters
---------------------------

1. If the installer is run against a single host, `pulp_content_bind` and `pulp_api_bind` are defaulted
   so that the webserver reverse proxies to the API server and content server running on the single host.  
   Thus there is no need to set any cluster variables for a single host.

2. If the installer is run against a single `pulp_content` host and a single `pulp_api` host, setting
   `pulp_content_bind` and `pulp_api_bind` is sufficient for the `pulp_webserver` host(s) to reverse proxy
   to them.  
   These 2 shared variables need to be set for both the `pulp_api`/`pulp_cluster` hosts, and the
   `pulp_webserver` hosts.  

    ```yaml
    pulp_api_bind: "example-pulp-api-server:24817"
    pulp_content_bind: "example-pulp-api-server:24816"
    ```

3. If the installer is run against multiple `pulp_content` hosts or multiple `pulp_api` hosts,
   it becomes necessary to set `pulp_api_bind` and `pulp_content_bind` in combination with
   `pulp_webserver_api_hosts` and `pulp_webserver_content_hosts`. These latter 2 variables
    set the reverse proxy behavior for when there are multiple servers to proxy to.  
   `pulp_api_bind` and `pulp_content_bind`
   only need to be set for the `pulp_api` and `pulp_content` hosts (they are not shared variables
   anymore), while `pulp_webserver_api_hosts` and `pulp_webserver_content_hosts` only need to
   be set for the `pulp_webserver` hosts.  
   Additionally, there are **optional** load balancing variables
   and optional load balancing nested variables, and they differ based on nginx or apache.  
   Here are 3 examples, the 1st example works for either `pulp_webserver_server==apache` or
   `pulp_webserver_server==nginx`, the latter 2 are specific to a apache/nginx.  

    ```yaml
    pulp_api_bind: "{{ ansible_facts.fqdn }}:24817"
    pulp_content_bind: "{{ ansible_facts.fqdn }}:24816"
    pulp_webserver_api_hosts:
      - address: "pulp-api1:24817"
      - address: "pulp-api2:24817"
    pulp_webserver_content_hosts:
      - address: "pulp-content1:24817"
      - address: "pulp-content2:24817"
    ```

    ```yaml
    pulp_webserver_server: nginx
    pulp_api_bind: "{{ ansible_facts.fqdn }}:24817"
    pulp_content_bind: "{{ ansible_facts.fqdn }}:24816"
    pulp_webserver_api_hosts:
      - address: "pulp-api1:24817"
        nginx_parameters:
          - weight=1
          - max_conns=100
      - address: "pulp-api2:24817"
        nginx_parameters:
          - weight=2
          - max_conns=100
    pulp_webserver_content_hosts:
      - address: "pulp-content1:24817"
        nginx_parameters:
          - weight=1
          - max_conns=100
      - address: "pulp-content2:24817"
        nginx_parameters:
          - weight=2
          - max_conns=100
    pulp_webserver_api_balancer_nginx_directives:
      - name: zone
        parameters:
        - upstream_dynamic
        - 64k
    pulp_webserver_content_balancer_nginx_directives:
      - name: zone
        parameters:
        - upstream_dynamic
    ```

    ```yaml
    pulp_webserver_server: apache
    pulp_api_bind: "{{ ansible_facts.fqdn }}:24817"
    pulp_content_bind: "{{ ansible_facts.fqdn }}:24816"
    pulp_webserver_api_hosts:
      - address: "pulp-api1:24817"
        apache_parameters:
          - keepalive=on
          - lbset=1
      - address: "pulp-api2:24817"
        apache_parameters:
          - keepalive=on
          - lbset=2
    pulp_webserver_content_hosts:
      - address: "pulp-content1:24817"
        apache_parameters:
          - keepalive=on
          - lbset=1
      - address: "pulp-content2:24817"
        apache_parameters:
          - keepalive=on
          - lbset=2
        - upstream_dynamic
    pulp_webserver_content_balancer_apache_parameters:
      - lbmethod=bytraffic
      - timeout=10
    pulp_webserver_api_balancer_apache_parameters:
      - lbmethod=bytraffic
      - timeout=10
    ```

    For more info on these optional load balancing variables:

    * `apache_parameters` for `pulp_webserver_api_hosts`/`pulp_webserver_content_hosts`: See the Apache "Worker|BalancerMember parameters" under [this link.](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxypass) (Note however that the servers ("BalancerMember") are not specified in the "url" format listed on the link, they must be specified in the "address" format (hostname:port or ip:port) as listed in these docs because pulp generates the URL.)
    * `pulp_webserver_content_balancer_apache_parameters`/`pulp_webserver_api_balancer_apache_parameters`: See the Apache "Balancer parameters" under [the same link as before.](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#proxypass)
    * `nginx_parameters` for `pulp_webserver_api_hosts`/`pulp_webserver_content_hosts`: See the
      Nginx server "parameters" under [this
    link.](http://nginx.org/en/docs/http/ngx_http_upstream_module.html#server)
    * `pulp_webserver_api_balancer_nginx_directives`/`pulp_webserver_content_balancer_nginx_directives`:
      See the Nginx "Directives" under [the same page as
    before.](http://nginx.org/en/docs/http/ngx_http_upstream_module.html)

Plugin Webserver Configs
------------------------

The installer copies config fragments from plugin Python packages, installed on the host that runs
the `pulp_api` role, to either nginx or apache on the `pulp_webserver` host.
These fragments typically provide additional url routing to either the Pulp API or
Pulp Content App. pulp_ansible has an example of such configs
[here](https://github.com/pulp/pulp_ansible/tree/main/pulp_ansible/app/webserver_snippets).

The Nginx config provides definitions for the location of the Pulp Content App and the Pulp API as
pulp-api and pulp-content respectively. To route the url `/pulp_ansible/galaxy/` to the Pulp API you
could use this definition in a snippet like:

```nginx
location /pulp_ansible/galaxy/ {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Host $http_host;
    # we don't want nginx trying to do something clever with
    # redirects, we set the Host: header above already.
    proxy_redirect off;
    proxy_pass http://pulp-api;
}
```

The Apache config provides variables containing the location of the Pulp Content App and the Pulp
API as pulp-api and pulp-content respectively. Below is an equivalent snippet to the one above, only
for Apache:

```apache
ProxyPass /pulp_ansible/galaxy http://${pulp-api}/pulp_ansible/galaxy
ProxyPassReverse /pulp_ansible/galaxy http://${pulp-api}/pulp_ansible/galaxy
```

Shared variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role is **not tightly coupled** to the `pulp_common` role, but uses some of the same
variables. When used in the same play, the values are inherited from the role.
When not used together, this role provides identical defaults.

* `pulp_certs_dir`: Path where to generate or drop the TLS certificates. Defaults to
  '{{ pulp_config_dir }}/certs' .
* `pulp_config_dir`: Directory under which pulp_certs_dir is created by default.
  Defaults to "/etc/pulp".
* `pulp_user_home`: equivalent to `MEDIA_ROOT` from `pulpcore` i.e. absolute path for pulp user home.
Parent directory for `pulp_webserver_static_dir`
* `pulp_content_bind` Set the host the reverse proxy should connect to for the Content app. Defaults
  to '127.0.0.1:24816'.
* `pulp_api_bind` Set the host the reverse proxy should connect to for the API server. Defaults
  to '127.0.0.1:24817'.
* `pulp_settings`: A nested dictionary that is used to add custom values to the user's
    `settings.py`. Used by `pulp_webserver` specifically to provide custom webserver configuration
     based on the values of `pulp_settings.api_root` and `pulp_settings.content_path_prefix`

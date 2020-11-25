pulp_webserver
==============

Install, configure, start, and enable a web server.

Currently, Nginx and Apache are supported. They are configured as a reverse proxy to the pulpcore-api
and pulpcore-content Gunicorn processes.

By default TLS will be enabled (with self-signed certificates if none are provided). An automatic
redirect from http to https will take place.


Role Variables
--------------

* `pulp_webserver_server` Set the webserver Pulp should use to reverse proxy with. Defaults to
  `nginx`. The other valid value is `apache`.
* `pulp_configure_firewall` Install and configure a firewall. Valid values are `auto`, `firewalld`,
  and `none`. Defaults to `auto` (which is the same as `firewalld`, but may change in the future).
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
- `pulp_webserver_static_dir` absolute path where to place static files, such as for the .well-known
   directory for ACME (letsencrypt) files or SSL certs. This is not to be confused with the Pulp
   application's setting `STATIC_ROOT`, which is a function of Pulp itself (not the webserver) and servces
   a different set of files.

Plugin Webserver Configs
------------------------

The installer symlinks config fragments from plugin Python packages to either nginx or apache during
installation. These fragments typically provide additional url routing to either the Pulp API or
Pulp Content App. pulp_ansible has an example of such configs [here](https://github.com/pulp/
pulp_ansible/tree/master/pulp_ansible/app/webserver_snippets).

The Nginx config provides definitions for the location of the Pulp Content App and the Pulp API as
pulp-api and pulp-content respectively. To route the url `/pulp_ansible/galaxy/` to the Pulp API you
could use this definition in a snippet like:

```
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

```
ProxyPass /pulp_ansible/galaxy http://${pulp-api}/pulp_ansible/galaxy
ProxyPassReverse /pulp_ansible/galaxy http://${pulp-api}/pulp_ansible/galaxy
```

Shared variables
----------------

* `ansible_python_interpreter`: **Required**. Path to the Python interpreter.

This role **is tightly coupled** to the required `pulp_common` role, and inherits
some of its variables.

* `pulp_certs_dir`: Path where to generate or drop the TLS certificates. Defaults to
  '{{ pulp_config_dir }}/certs' .
* `pulp_install_dir`: Location of a virtual environment for Pulp and its Python
  dependencies.
* `pulp_install_plugins` (technically `pulp_install_plugins_normalized`). The list
  of plugins to install is used to inform pulp_webserver which webserver snippets
  to look for and use.
* `pulp_user_home`: equivalent to `MEDIA_ROOT` from `pulpcore` i.e. absolute path for pulp user home.
* `pulp_content_bind` Set the host the reverse proxy should connect to for the Content app. Defaults
  to '127.0.0.1:24816'.
* `pulp_api_bind` Set the host the reverse proxy should connect to for the API server. Defaults
  to '127.0.0.1:24817'.

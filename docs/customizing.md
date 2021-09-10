Customizing Your Pulp Deployment
================================

Background info on Ansible variables
------------------------------------

Because the Pulp Installer is based on Ansible, it inherits two Ansible designs:

1. Variables can be set in many different ways by the user.
2. Each role has a set of variables it recognizes for customizing the deployment.

This section (and the docs in general) will not cover every possible way of [setting variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#where-to-set-variables), but instead cover the
simplest way: in the Ansible "playbook" itself.

This means that the playbook, like listed in [Getting Started](quickstart.md#example-playbook-for-installing-plugins), has a section `vars:`.

This section intends to demonstrate how to use Ansible variables to configure Pulp rather than listing every variable. Documentation for each Ansible variable can be found in each [Ansible role's README file.](index.md#roles)

Note that [variables are YAML](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html#yaml-basics) and have types such as dictionaries (key-value pairs), lists, strings and booleans.

(JSON can also be used as values to the variables.)

Some of the installer's variables, `pulp_settings` and `pulp_install_plugins` in particular, are dictionaries with prescribed variables or prescribed nested dictionaries nested under them. So do not be surprised when you see syntax like the following:
```
  vars:
    pulp_install_plugins:
       pulp-container: {}
       pulp-deb:
         upgrade: true
      pulp-file:
        collectstatic: true
        version: "9.8.7"
```

What that means **in terms of YAML syntax** is:
* There is a dictionary named `pulp_install_plugins` whose value is 3 nested dictionaries, `pulp-deb`, `pulp-file` and `pulp-container`.
* There is a nested dictionary named `pulp-container` dictionary, whose value is an empty dictionary `{}`.
* There is a nested dictionary named `pulp-deb`, whose value is is 1 key-value pair.
* There is a nested dictionary named `pulp-file`, whose value is 2 key-value pairs.

See [the section below](#example-of-setting-a-multitude-of-variables) for more info on what this means in terms of actual Pulp Installer behavior.


Pulp Installer's types of Variables
-----------------------------------
Generally, there are 3 categories of variables
1. Those that make pulp_installer compatible with your environment. For example, the firewall.
2. Preferences for how Pulp is configured and deployed. In particular, which plugins to install.
3. Variables to control which version of plugins are installed.

WRT to #2, the large data structure variables are `pulp_settings` & `pulp_install_plugins`.
WRT to #3, the large data structure variable is `pulp_install_plugins`.

Because the Pulp installer is composed of Ansible roles, you can use the variables for each of these roles to customize your Pulp installation.
For example, if you want to specify firewall requirements, edit the corresponding firewall variables associated with the [pulp_webserver](https://docs.pulpproject.org/pulp_installer/roles/pulp_webserver/#pulp_webserver) role.
[Each role](index.md#roles) documents all the variables that it uses, including variables used by
other Pulp Installer roles ("Shared Variables.")

**Required Variables:**
Most variables have generally compatible default values but a few are required (must be specified by the user). See ``playbooks/example-use/group_vars/all`` for
the minimal set of required variables.

Example of setting a multitude of variables:
--------------------------------------------
In the following example, a multitude of variables are set:

```
  vars:
    pulp_workers: 4
    pulp_install_plugins:
      pulp-container: {}
      pulp-deb:
        upgrade: true
      pulp-file:
        collectstatic: true
        version: "9.8.7"
    pulp_settings:
      secret_key: secret
      content_origin: "{{ pulp_webserver_disable_https | default(false) | ternary('http', 'https') }}://{{ ansible_fqdn }}"
      azure_account_name: 'Storage account name'
      azure_container: 'Container name (as created within the blob service of your storage account)'
      azure_account_key: 'Key1 or Key2 from the access keys of your storage account'
      azure_url_expiration_secs: 60
      azure_overwrite_files: 'True'
      azure_location: 'the folder within the container where your pulp objects will be stored'
      default_file_storage: 'storages.backends.azure_storage.AzureStorage'
```

`pulp_workers`, is set to `4`, which means that 4 worker processes will be started for processing jobs on a multi-core system. It replaces the default value of 2.

`pulp_install_plugins` does the following:
* Directs the installer to install all 3 plugins, pulp-deb, pulp-file and pulp-container.
* If pulp-container is not installed, the latest version will be installed.
* If pulp-container is already installed, the current version will be left intact.
* If pulp-deb is not installed, the latest version will be installed.
* If pulp-deb is already installed, it will be upgraded to the latest version.
* If pulp-file is not installed, version `9.8.7` will be installed.
* If pulp-file is already installed, it will be upgraded to `9.8.7`.
* pulp-file's static files will be collected at install time. (`true` is the default behavior for every plugin, and pulp-file requires this. So it did not need to be specified. However, it is listed for syntax demonstration purposes, and sometimes plugin will instruct you to set it to `false`.)


`pulp_settings` does the following:
* It generates Pulp's runtime configuration file, `/etc/pulp/settings.py`, with all of the following configured behavior.
  * `default_file_storage` and `azure_*` configure pulp to point to an object storage on Azure for
    storing content (rather than defaulting to using the local filesystem.)
  * It sets the `secret_key` for the Django framework (which) Pulp is written in) to `"secret"`. Note that this setting is always required to be set by the user.
  * It sets `content_origin`, which specifies the Pulp application's URL, to the FQDN (`hostname -a`) of the Pulp server (beginning with `https://`). Note that this setting is always required to be set by the user, although this example value (with variables in it) is suitable for most users.

More information about `pulp_settings`
* Please do not modify `/etc/pulp/settings.py` manually after install, because re-running the installer for upgrades / repairing Pulp will revert your changes. Please re-run the installer instead with your changes added to `pulp_settings`.
* `pulp_settings` is used during both the installation process (it can cause errors at install time with incorrect values), and once pulp is installed.

Explanation of plugin version compatibility with Pulpcore
--------------------------------------------------

Pulp 3 has a plugin architecture so that new content types and features can be added by the
larger community. However, both pulpcore & plugins are installed by the installer using `pip`, which has limited
dependency resolution. Plugins release at their own lifecycles. Thus in the worst case scenario, the
latest release of plugin pulp_juicy could depend on the current minor version (e.g., 3.10.z) of
pulpcore, while the latest release of pulp_sugary could depend on only older versions of pulpcore
(e.g., 3.8.z or 3.9.z).

In order to avoid breaking multiple plugins for the sake of one plugin, and to avoid breaking existing
installations, upgrading a plugin will not cause pulpcore to be updated as a dependency. Similarly,
if there is an attempt to update a plugin to a version that is incompatible with pulpcore, the installer
will fail and exit. The installer does a compatibility check early in the installation to prevent Pulp
from being installed or upgraded to an incompatible state.

Thus you, yourself, must research plugin compatibility with the pulpcore version whenever you are
installing one or more plugins. With each plugin release, the plugin compatibility is announced as
part of the release announcement and included in the documentation for the specific plugin.

Recommended Workflows for Pulpcore & Plugin Versioning
------------------------------------------------------

### Latest Version with Minimal Effort:

Initial installation:

1. Make sure you are running the latest version of the installer, which installs pulpcore's
   latest version.
1. Confirm that all the latest stable releases of your desired plugins are compatible with
   pulpcore's latest version , such as by reading the release announcement email thread for
   pulpcore's latest version, reading the plugins README, or as a last resort, reading their `setup.py`.
1. Set `pulp_install_plugins` with each plugin listed as a key, with an empty enum '{}' as each plugin's value.
1. Run `pulp_installer`.
1. Make sure to save your variables/playbook for later usage.

Example `pulp_install_plugins`:
```
  vars:
    pulp_install_plugins:
      pulp-container: {}
      pulp-file: {}
      pulp-rpm: {}
```

Upgrading your installation:

1. Observe what is the latest version of `pulp_installer`, and what version of pulpcore it installs.
1. Confirm that all the latest stable releases of all **currently installed** plugins are compatible
   with pulpcore's latest version, such as by reading the release announcement email thread for pulpcore's
   latest version, reading the plugins' README files, or as a last resort, reading their setup.py.
1. If they are not all compatible yet, **wait** for the plugins to be updated for
   compatibility.
1. Upgrade `pulp_installer` to the latest version.
1. Set `pulp_install_plugins` with each plugin listed as a key, and with each plugin having a key under it called `upgrade` set to the value `true`.
1. Re-run `pulp_installer`.
1. Make sure to save your variables/playbook for later usage.

Example `pulp_install_plugins`:
```
  vars:
    pulp_install_plugins:
      pulp-container:
         upgrade: true
      pulp-file:
         upgrade: true
      pulp-rpm:
         upgrade: true
```

### Specifying Exact Versions with Reproducibility:

Initial installation:

1. Observe the latest branch of `pulp_installer`, and what version of pulpcore it installs.
1. Confirm that all the latest stable releases of your desired plugins are compatible with
   pulpcore's latest version, such as by reading the release announcement email thread for
   pulpcore's latest version, reading the plugins README, or as a last resort, reading their setup.py.
1. If they are not all compatible yet, try the last version of the installer that installs
   pulpcore's previous minor release (e.g., 3.9.z if 3.10.z were the latest). Then confirm that
   there exist stable releases of your desired plugins that are compatible with pulpcore's
   previous minor release. If there are none, try the minor release before that (e.g., 3.8.z) and
   repeat.
1. Once a compatible pulpcore version is found, Set `pulp_install_plugins` with each plugin listed
   as a key, and with each plugin having a key under it called `version` set to the version as the
   value (with quotes).
1. Run `pulp_installer`
1. Make sure to save your variables/playbook for later usage.

Example `pulp_install_plugins` (with bogus version values):
```
  vars:
    pulp_install_plugins:
      pulp-container:
         version: "4.5.6"
      pulp-file:
         version: "5.6.7"
      pulp-rpm:
         version: "6.7.8"
```


Upgrading your install:

1. Observe what the latest version of `pulp_installer` is, and what version of pulpcore it installs
   (Even if there is no update, you can still upgrade your plugins.)
1. Confirm that all the latest stable releases of **currently installed** plugins are compatible
   with pulpcore's latest version, such as by reading the release announcement email thread for
   pulpcore's latest version, reading the plugins' README files, or as a last resort, reading their
   setup.py.
1. If they are not all compatible yet, try the last version of the installer that installs
   pulpcore's previous minor release (e.g., 3.9.z if 3.10.z were the latest). Then confirm that
   there exist stable releases of your desired plugins that are compatible with pulpcore's
   previous minor release. If there are none, try the minor release before that (e.g., 3.8.z) and
   repeat. (But do not try to downgrade pulpcore to an older version than you have installed.)
1. Once a compatible pulpcore version is found, Set `pulp_install_plugins` with each plugin listed
   as a key, and with each plugin having a key under it called `version` set to the **new** version
   as the value (with quotes).
1. Upgrade `pulp_installer` to the specified version. If there is a post-release for the desired
   version (such as 3.10.0-1 versus 3.10.0), upgrade to the latest post-release.
1. Run `pulp_installer`
1. Make sure to save your variables/playbook for later usage.


Example `pulp_install_plugins` (with bogus version values):
```
  vars:
    pulp_install_plugins:
      pulp-container:
         version: "5.6.7"
      pulp-file:
         version: "6.7.8"
      pulp-rpm:
         version: "7.8.9"
```

Deployment Scenarios
--------------------

In this section, you can find information and Ansible playbook examples that demonstrate how to
configure the following installation scenarios:

* [A single “all-in-one” Pulp server that includes the database, redis, and webserver.](#all-in-one-pulp-server-example)
* [Pulp on one server, while using existing servers for the database, redis, and webserver.](#pulp-server-with-existing-infrastructure)
* [Pulp on one server, with the database, redis & webserver on separate servers.](#pulp-with-separate-servers-for-services)
* [Each and every Pulp service on a separate server.](#separate-servers-for-each-and-every-service)

Depending on your requirements for high availability and better scalability, you might like to
customize your installations according to these examples.


#### 'All in One Pulp Server' Example

This deployment consists of installing a single server that contains all Pulp services, including
the database, redis & webserver.

```
---
- hosts: example-pulp-server
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://"
    pulp_install_plugins:
      pulp-container: {}
      pulp-rpm: {}
  roles:
    - pulp_all_services
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```    

#### Pulp Server with Existing Infrastructure

This deployment consists of a single Pulp server that relies on an existing database and existing redis server. No new servers are used or created.

```
---
- hosts: example-pulp-server
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_content_bind: example-pulp-server:24816
    pulp_api_bind: example-pulp-server:24817
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-webserver.fqdn"
      redis_host: example-existing-redis-server
      redis_port: 6379
      redis_password: << YOUR REDIS PASSWORD HERE >>
      databases:
        default:
          HOST: example-existing-postgres-server
          ENGINE: django.db.backends.postgresql_psycopg2
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container: {}
      pulp-rpm: {}
  roles:
    - pulp_services
    - pulp_webserver
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```

#### Pulp with Separate Servers for Services

This scenario has the following layout:

* Pulp on one server
* The database on a second server
* redis on a third server
* The webserver on a fourth server

Note that `pulp_webserver` still depends on `pulp_common` to provide the python packages for the
per-plugin webserver snippets. This means that the webserver will have pulpcore and all plugins
installed on it but no code will be running.

```
---
- hosts: example-postgres-server
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
  vars:
    pulp_redis_bind: 'example-redis-server:6379'
  roles:
    - pulp_redis

- hosts: example-pulp-server
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_content_bind: example-pulp-server:24816
    pulp_api_bind: example-pulp-server:24817
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-webserver.fqdn"
      redis_host: example-redis-server
      redis_port: 6379
      databases:
        default:
          HOST: example-postgres-server
          ENGINE: django.db.backends.postgresql_psycopg2
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container: {}
      pulp-rpm: {}
  roles:
    - pulp_services
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts: example-webserver
  vars:
    pulp_content_bind: example-pulp-server:24816
    pulp_api_bind: example-pulp-server:24817
  roles:
    - pulp_webserver
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```

#### Separate Servers for Each and Every service

In this deployment, every single service is deployed on its own server.

Note that `pulp_webserver` still depends on `pulp_common` to provide the python packages for the
per-plugin webserver snippets. This means that the webserver will have pulpcore and all plugins
installed on it but no code will be running.

In this example, there are two Pulp worker servers.

```
---
- hosts: example-postgres-server
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
  vars:
    pulp_redis_bind: 'example-redis-server:6379'
  roles:
    - pulp_redis

- hosts: example-pulp-api-server
  vars:
    pulp_default_admin_password: << YOUR PASSWORD FOR THE PULP APPLICATION HERE >>
    pulp_api_bind: example-pulp-api-server:24817
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-webserver.fqdn"
      redis_host: example-redis-server
      redis_port: 6379
      databases:
        default:
          HOST: example-postgres-server
          ENGINE: django.db.backends.postgresql_psycopg2
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container: {}
      pulp-rpm: {}
  roles:
    - pulp_api
    - pulp_database_config
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts: example-pulp-content-server
  vars:
    pulp_content_bind: example-pulp-content-server:24816
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://example-webserver.fqdn"
      redis_host: example-redis-server
      redis_port: 6379
      databases:
        default:
          HOST: example-postgres-server
          ENGINE: django.db.backends.postgresql_psycopg2
          NAME: pulp
          USER: pulp
          PASSWORD: << YOUR DATABASE PASSWORD HERE >>
    pulp_install_plugins:
      pulp-container: {}
      pulp-rpm: {}
  roles:
   - pulp_content
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts:
   - example-pulp-worker-server1
   - example-pulp-worker-server2
  vars:
   pulp_settings:
     secret_key: << YOUR SECRET HERE >>
     content_origin: "http://example-webserver.fqdn"
     redis_host: example-redis-server
     redis_port: 6379
     databases:
       default:
         HOST: example-postgres-server
         ENGINE: django.db.backends.postgresql_psycopg2
         NAME: pulp
         USER: pulp
         PASSWORD: << YOUR DATABASE PASSWORD HERE >>
   pulp_install_plugins:
     pulp-container: {}
     pulp-rpm: {}
  roles:
   - pulp_workers
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts: example-resource-manager-server
  vars:
   pulp_settings:
     secret_key: << YOUR SECRET HERE >>
     content_origin: "http://example-webserver.fqdn"
     redis_host: example-redis-server
     redis_port: 6379
     databases:
       default:
         HOST: example-postgres-server
         ENGINE: django.db.backends.postgresql_psycopg2
         NAME: pulp
         USER: pulp
         PASSWORD: << YOUR DATABASE PASSWORD HERE >>
   pulp_install_plugins:
     pulp-container: {}
     pulp-rpm: {}
  roles:
   - pulp_resource_manager
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings

- hosts: example-webserver
  vars:
   pulp_content_bind: example-pulp-server:24816
   pulp_api_bind: example-pulp-server:24817
  roles:
   - pulp_webserver
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```

Note that the `example-pulp-api-server` is also used to to run `pulp_database_config`.
This means that it will create and migrate the database for Pulp.
The name `example-pulp-api-server` follows an Ansible standard that implies that more can be added at a later stage.

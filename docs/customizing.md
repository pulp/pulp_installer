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

This section intends to demonstrate how to use Ansible variables to configure Pulp rather than listing every variable. Documentation for every Ansible variable can be found in each [Ansible role's README file.](index.md#roles)

Note that [variables are YAML](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html#yaml-basics) and have types such as dictionaries (key-value pairs), lists, strings and booleans.

(JSON can also be used as values to the variables.)

Some of the installer's variables, `pulp_settings` and `pulp_install_plugins` in particular, are dictionaries with prescribed variables or prescribed nested dictionaries nested under them. So do not be surprised when you see syntax like the following:

```yaml
  vars:
    pulp_install_plugins:
       pulp-container:
       pulp-deb:
         upgrade: true
       pulp-file:
         collectstatic: true
         version: "9.8.7"
```

What that means **in terms of YAML syntax** is:

* There is a dictionary named `pulp_install_plugins` whose value is 3 nested dictionaries, `pulp-deb`, `pulp-file` and `pulp-container`.
* There is a nested dictionary named `pulp-container`, whose value is an empty dictionary `{}`.
* There is a nested dictionary named `pulp-deb`, whose value is 1 key-value pair.
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

```yaml
  vars:
    pulpcore_update: true
    pulp_workers: 4
    pulp_install_plugins:
      pulp-container:
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

`pulpcore_update` is set to `true` which means that if pulpcore 3.16 is already installed, it will be upgraded to the latest patch release 3.16.z.

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
  * It sets the `secret_key` for the Django framework (which Pulp is written in) to `"secret"`. Note that this setting is always required to be set by the user.
  * It sets `content_origin`, which specifies the Pulp application's URL, to the FQDN (`hostname -a`) of the Pulp server (beginning with `https://`). Note that this setting is always required to be set by the user, although this example value (with variables in it) is suitable for most users.

More information about `pulp_settings`

* Please do not modify `/etc/pulp/settings.py` manually after install, because re-running the installer for upgrades / repairing Pulp will revert your changes.
  Please use `/etc/pulp/settings.local.py` to keep your local pulp settings or re-run the installer instead with your changes added to `pulp_settings`.
    * List of available setting in [pulpcore docs](https://docs.pulpproject.org/pulpcore/configuration/settings.html) and format follows [dynaconf syntax](https://dynaconf.readthedocs.io/en/docs_223/guides/examples.html#py).
* `pulp_settings` is used during both the installation process (it can cause errors at install time with incorrect values), and once pulp is installed.

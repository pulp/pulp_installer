Pulp 3 Ansible Installer
========================

The Pulp 3 Ansible installer is a collection of Ansible roles that you can use to install or upgrade Pulp 3, as well as reconfigure or add plugins to an existing installation.

Each Ansible role installs and configures a component of Pulp.

This version of the installer, 3.9.0-1, installs Pulp 3.9.0 specifically.

If run against an older version of Pulp 3, it will upgrade it to 3.9.0.

System Requirements
-------------------

The [control node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#control-node)
must have Python 3 and Ansible (>= 2.9) installed.

The [managed node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#managed-nodes)
must be one of these currently supported operating systems:

- CentOS 7
- Debian Buster (needs `allow_world_readable_tmpfiles = True` in ansible.cfg)
- Fedora 30 or later

The managed node cannot provide any other service on the same hostname as Pulp's API. The only
exception is Pulp 2. The RESP APIs for Pulp 2 and Pulp 3 can be served on the same hostname as
long as the `apache` webserver is deployed for both.

The Ansible collection requires [geerlingguy.postgresql](https://galaxy.ansible.com/geerlingguy/postgresql) role,
which should be installed from ansible-galaxy.

```
ansible-galaxy install geerlingguy.postgresql
```

Variables
---------

**Each role documents all the variables that it uses**. Some variables are
used by multiple roles. In that case, they are documented in their primary role and mentioned in
the `shared_variables` section the other roles.

**Required Variables:**
Most variables have sane defaults but a few are required. See ``playbooks/example-use/group_vars/all`` for
the minimal set of required variables.


Ansible Boilerplate
-------------------

These roles can be used against any managed node and are highly configurable.  Knowledge of
[ansible basics](https://docs.ansible.com/ansible/2.5/user_guide/intro_getting_started.html) will
be helpful, but even if you are new to Ansible, this section will get you started, or you can try
the Vagrant installations to bypass the Ansible boilerplate.

First, you will need to configure SSH between your control node and your managed node. When you can
SSH into the managed node without a password, you are ready to move to the next step.

Next, add the managed node's hostname or IP address to `/etc/ansible/hosts`.

Ensure that Ansible can communicate with the managed node.

```
ansible all -m ping -u <managed_node_username>
```

Note on Plugin Version Compatibility with Pulpcore
--------------------------------------------------

Pulp 3 has a plugin architecture so that new content types and features can be added by the
larger community. However, both pulpcore & plugins are installed via pip, which has limited
dependency resolution. Plugins release at their own lifecycles. Thus in the worst case scenario, the
2 stable branches of plugin pulp_juicy could depend on the current branch of pulpcore, while the 2
stable branches of pulp_sugary could depend on an older branch of pulpcore.

In order to avoid breaking multiple plugins for the sake of one plugin, and to avoid breaking existing
installations, upgrading a plugin will not cause pulpcore to be updated as a dependency. Similarly,
if there is an attempt to update a plugin to a version that is incompatible with pulpcore, the installer
will fail and exit. The installer does a compatibility check early in the installation to prevent Pulp
from being installed or upgraded to an incompatible state.

Thus you, yourself, must research plugin compatibility with the pulpcore version whether you are
installing one or more plugins.

Recommended Workflows for Pulpcore & Plugin Versioning
------------------------------------------------------

### Latest Version with Minimal Work Overview:

Initial installation:

1. Make sure you are running the latest version of the installer, which installs the latest version
   of pulpcore (3.9.0).
1. Confirm that all the latest stable releases of your desired plugins are compatible with pulpcore
   3.9.0, such as by reading the release announcement email thread for pulpcore 3.9.0, reading the
plugins README, or as a last resort, reading their `setup.py`.
1. Run `pulp_installer`.

Upgrading your installation:

1. Observe what is the latest version of `pulp_installer`, and what version of pulpcore it installed
   (3.9.0).
1. Confirm that all the latest stable releases of **currently installed** plugins are compatible
   with pulpcore 3.9.0, such as by reading the release announcement email thread for pulpcore 3.9.0,
reading the plugins README, or as a last resort, reading their setup.py.
1. If they are not all compatible yet, **wait** for the plugins to be updated for
   compatibility.
1. Upgrade `pulp_installer` to the latest version.
1. Re-run the `pulp_installer` with `upgrade` set to `true` for each plugin under
   `pulp_install_plugins`

### Specifying Exact Versions with Reproducibility

Initial installation:

1. Observe the latest branch of `pulp_installer`, and what version of pulpcore it installs (3.9.0).
1. Confirm that all the latest stable releases of your desired plugins are compatible with pulpcore
   3.9.0, such as by reading the release announcement email thread for pulpcore 3.9.0, reading the
plugins README, or as a last resort, reading their setup.py.
1. If they are not all compatible yet, try the last version of the installer that installs pulpcore
   3.9.z . Then confirm that there exist stable releases of your desired plugins that are compatible
with pulpcore 3.9.z. If there are none, try pulpcore 3.8.z, and repeat.
1. Once a compatible pulpcore version is found, specify `version` for each plugin under
   `pulp_install_plugins`.
1. Run `pulp_installer`

Upgrading your install:

1. Observe what the latest version of `pulp_installer` is, and what version of pulpcore it installed
   (3.9.0). (Even if there is no update, you can still upgrade your plugins.)
1. Confirm that all the latest stable releases of **currently installed** plugins are compatible
   with pulpcore 3.9.0, such as by reading the release announcement email thread for pulpcore 3.9.0,
reading the plugins README, or as a last resort, reading their setup.py.
1. If they are not all compatible yet, try the last version of the installer that installs pulpcore
   3.9.z . Then confirm that there exist stable releases of your desired plugins that are compatible
with pulpcore 3.9.z. If there are none, try pulpcore 3.8.z, and repeat.
1. Once a compatible pulpcore version is found, **revise** `version` for each plugin under
   `pulp_install_plugins`. Do not specify `upgrade` as well.
1. Upgrade `pulp_installer` to the latest version (if there is a new version.)
1. Run `pulp_installer`

Roles
-----

`pulp_installer` is equipped with the following roles:

- [pulp_common](roles/pulp_common): installs shared components of the Pulp 3 services from PyPi or source and provides basic config
- [pulp_api](roles/pulp_api): install, configure, and set the state of pulp API service
- [pulp_content](roles/pulp_content): install, configure, and set the state of pulp content app.
- [pulp_database](roles/pulp_database): install a suitable database server for Pulp 3
- [pulp_database_config](roles/pulp_database_config): configure the database for Pulp 3
- [pulp_redis](roles/pulp_redis): install and start Redis, and install RQ in the Pulp virtualenv.
- [pulp_resource_manager](roles/pulp_resource_manager): install, configure, and set the state of the pulp resouce manager.
- [pulp_webserver](roles/pulp_webserver): install, configure, start, and enable a web server.
- [pulp_workers](roles/pulp_workers): install, configure, and set the state of pulp workers.
- [pulp_devel](roles/pulp_devel): installs useful tools and adds some config files for a Pulp 3 development environment.

pulp_installer also is equipped with these prereq roles that perform additional tasks to install specific plugins:

- [pulp_rpm_prerequisites](/prereq_roles/pulp_rpm_prerequisites): installs prerequisites for pulp-rpm plugin use

pulp_installer also provides the following meta roles, which depend on a set of other roles. These provide
the convenience of writing playbooks that specify one role, rather than a list of roles that often changes.

- [pulp_all_services](meta_roles/pulp_all_services/): A role to install all Pulp services (first-party & third-party) on a single host.
- [pulp_services](meta_roles/pulp_services/): A role to install & configure Pulp's
  first-party services (including the state of the Pulp database) on a single host.

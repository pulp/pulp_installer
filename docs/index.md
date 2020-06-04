Pulp 3 Ansible Installer
========================

A collection of roles to install or upgrade Pulp 3. Can also reconfigure or add plugins to an existing install.

The Pulp 3 Ansible Installer consists of a collection of roles. Each role installs and configures a
component of Pulp. The roles are not currently available on Ansible Galaxy; to run the Pulp 3
Ansible installer, the [pulp_installer](https://github.com/pulp/pulp_installer) git repository must
be cloned or downloaded.

This version of the installer, 3.4.1, installs Pulp 3.4.1 specifically.

If run against an older version of Pulp 3, it will upgrade it to 3.4.1.

System Requirements
-------------------

The [control node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#control-node)
must have Python 3 and Ansible (>= 2.8) installed.

The [managed node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#managed-nodes)
must be one of these currently supported operating systems:
* CentOS 7
* Debian Buster (needs `allow_world_readable_tmpfiles = True` in ansible.cfg)
* Fedora 30 or later

Ansibles Python interpreter must have the package installed:
* psycopg2
* firewall (if firewalld should be configured; you can disable that with `pulp_configure_firewall=false`)

Variables
---------

**Each role documents all the variables that it uses**. Some variables are
used by multiple roles. In that case, they are be documented in their primary role and mentioned in
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

First, you will need to configure ssh between your control node and your managed node. When you can
ssh into the managed node without a password, you are ready to move to the next step.

Next, add the managed node's hostname or ip address to `/etc/ansible/hosts`.

It may be helpful to ensure that Ansible can communicate with the managed node.

```
ansible all -m ping -u <managed_node_username>
```

Note on Plugin Version Compatibility with Pulpcore
--------------------------------------------------

Pulp 3 has a plugin architecture so that new content types, and new features, can be added by the
larger community. However, both pulpcore & plugins are installed via pip, which has limited
dependency resolution. Plugins release at their own lifecycles. Thus in the worst case scenario, the
2 stable branches of plugin pulp_juicy could depend on the current branch of pulpcore, while the 2
stable branches of pulp_sugary could depend on an older branch of pulpcore.

In order to avoid breaking multiple plugins for the sake of 1 plugin, and to avoid breaking existing
installs, upgrading a plugin will not cause pulpcore to be updated as dependency. Similarly, if a
plugin were to be attempted to be updated to an incompatible version with pulpcore, the installer
will fail & exit. The installer does a compatibility check early in the installation to prevent Pulp
from being installed/upgraded to an incompatible state.

Thus you, yourself, must research plugin compatibility with the pulpcore version whether you are
installing 1 plugin, or more than 1 plugin.

Recommended Workflows for Pulpcore & Plugin Versioning
-----------------------------------------------------

### Latest Version with Minimal Work:

Initial install:

1. Make sure you are running the latest version of the installer, which installs the latest version
   of pulpcore (3.4.1).
1. Confirm that all the latest stable releases of your desired plugins are compatible with pulpcore
   3.4.1, such as by reading the release announcement email thread for pulpcore 3.4.1, reading the
plugins README, or as a last resort, reading their setup.py.
1. Run pulp_installer.

Upgrading your install:

1. Observe what the latest version of pulp_installer is, and what version of pulpcore it installed
   (3.4.1).
1. Confirm that all the latest stable releases of **currently installed** plugins are compatible
   with pulpcore 3.4.1, such as by reading the release announcement email thread for pulpcore 3.4.1,
reading the plugins README, or as a last resort, reading their setup.py.
1. If they are not all compatible yet, hold off & **wait** for the plugins to be updated for
   compatibility.
1. Upgrade pulp_installer to the latest version.
1. re-run the pulp_installer with `upgrade` set to `true` for each plugin under
   `pulp_install_plugins`

### Specifying Exact Versions with Reproducibility

Initial install:

1. Observe the latest branch of pulp_installer, and what version of pulpcore it installs (3.4.1).
1. Confirm that all the latest stable releases of your desired plugins are compatible with pulpcore
   3.4.1, such as by reading the release announcement email thread for pulpcore 3.4.1, reading the
plugins README, or as a last resort, reading their setup.py.
1. If they are not all compatible yet, try the last version of the installer that installs pulpcore
   3.3.z . Then confirm that there exist stable releases of your desired plugins that are compatible
with pulpcore 3.3.z. If there are none, try pulpcore 3.2.z, and repeate.
1. Once a compatible pulpcore version is found, specify `version` for each plugin under
   `pulp_install_plugins`.
1. Run pulp_installer

Upgrading your install:

1. Observe what the latest version of pulp_installer is, and what version of pulpcore it installed
   (3.4.1). (Even if there is no update, you can still upgrade your plugins.)
1. Confirm that all the latest stable releases of **currently installed** plugins are compatible
   with pulpcore 3.4.1, such as by reading the release announcement email thread for pulpcore 3.4.1,
reading the plugins README, or as a last resort, reading their setup.py.
1. If they are not all compatible yet, try the last version of the installer that installs pulpcore
   3.3.z . Then confirm that there exist stable releases of your desired plugins that are compatible
with pulpcore 3.3.z. If there are none, try pulpcore 3.2.z, and repeat.
1. Once a compatible pulpcore version is found, **revise** `version` for each plugin under
   `pulp_install_plugins`. Do not specify `upgrade` as well.
1. Upgrade pulp_installer to the latest version (if there is a new version.)
1. Run pulp_installer

Roles
-----

pulp_installer is equipped with the following roles:

- [pulp](roles/pulp/): installs Pulp 3 from PyPi or source and provides basic config.
- [pulp_content](roles/pulp_content): install, configure, and set the state of pulp content app.
- [pulp_database](roles/pulp_database): optionally install a database, then configure for Pulp.
- [pulp_redis](roles/pulp_redis): install and start Redis, and install RQ in the Pulp virtualenv.
- [pulp_resource_manager](roles/pulp_resource_manager): install, configure, and set the state of the pulp resouce manager.
- [pulp_webserver](roles/pulp_webserver): install, configure, start, and enable a web server.
- [pulp_workers](roles/pulp_workers): install, configure, and set the state of pulp workers.
- [pulp_devel](roles/pulp_devel): installs useful tools and adds some config files for a Pulp 3 development environment.

Pulp 3 Ansible Installer
========================

The Pulp 3 Ansible installer is a collection of Ansible roles that you can use to install or upgrade Pulp 3, as well as reconfigure or add plugins to an existing installation.

Each Ansible role installs and configures a component of Pulp.

This version of the installer, 3.15.2-2, installs Pulp 3.15.2 specifically.

If run against an older version of Pulp 3, it will upgrade it to 3.15.2.

---
**Didn't find what you need to get started?**

We are actively trying to make our documentation as complete and user-friendly as possible.
If you experience any difficulties or have any feedback, write to `pulp-list@redhat.com`.
[Documentation PRs](https://github.com/pulp/pulp_installer/edit/master/docs/index.md) are always welcome.
---


System Requirements
-------------------

Before you install Pulp, review the [architecture and component documentation](https://docs.pulpproject.org/pulpcore/components.html#) to ensure you understand the deployment structure and concepts.

The Ansible [control node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#control-node)
(i.e., your workstation) must have Python 3 and Ansible (>= 2.9) installed.

Ensure that your server meets the [hardware requirements](https://docs.pulpproject.org/pulpcore/components.html#hardware-requirements) to install and run Pulp.

Ensure that your server, AKA the Ansible [managed node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#managed-nodes),
runs one of these currently supported operating systems:

- CentOS 7 or 8
- Debian Bullseye (needs `allow_world_readable_tmpfiles = True` in ansible.cfg)
- Fedora 32 or later

The server cannot provide any other HTTP (port 80, 443) service on the same hostname as Pulp's API. The only
exception is Pulp 2. The REST APIs for Pulp 2 and Pulp 3 can be served on the same hostname as
long as the `apache` webserver is deployed for both.

NOTE: These server requirements assume you are deploying Pulp to a single server. If you are deploying it
to a cluster (with multiple tiers), the hardware requirements will differ, and only the webserver
(`pulp_webserver` role) will have the service limitation. Each node must run a supported operating
system from the list above, but each node can run a different OS.

The Ansible collection requires [geerlingguy.postgresql](https://galaxy.ansible.com/geerlingguy/postgresql) role,
which you can install on the Ansible control node from ansible-galaxy.

```
ansible-galaxy install geerlingguy.postgresql
```

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

`pulp_installer` also is equipped with these prereq roles that perform additional tasks to install specific plugins:

- [pulp_rpm_prerequisites](prereq_roles/pulp_rpm_prerequisites): installs prerequisites for pulp-rpm plugin use

`pulp_installer` also provides the following meta roles, which depend on a set of other roles. These provide
the convenience of writing playbooks that specify one role, rather than a list of roles that often changes.

- [pulp_all_services](meta_roles/pulp_all_services/): A role to install all Pulp services (first-party & third-party) on a single host.
- [pulp_services](meta_roles/pulp_services/): A role to install & configure Pulp's
  first-party services (including the state of the Pulp database) on a single host.

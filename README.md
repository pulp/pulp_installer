ansible-pulp3
=============

Pulp 3 Ansible installer.

The Pulp 3 Ansible installer consists of several roles. Each role installs and
configures a component of Pulp. For example, the `pulp3-postgresql` role
installs and configures PostgreSQL. The roles are not available on Ansible
Galaxy. (This may change in the future.) To run the Pulp 3 Ansible installer,
the [ansible-pulp3](https://github.com/pulp/ansible-pulp3) git repository must
be cloned.

The ansible-pulp3 repository contains a playbook, group vars, host vars, and so
on. However, these files are used by the test harness, and *must not* be relied
upon. To reliably run the Ansible Pulp 3 installer, create your own playbook,
group vars, host vars, and so on.

For example, let's say you have virtual machines with hostnames
`centos-7-pulp-3`, `fedora-27-pulp-3`, and `fedora-28-pulp-3`. Let's also say
that you've configured passwordless SSH, and that the remote Ansible users have
passwordless sudo access. You can install Pulp 3 on them with the following
script:

```bash
cat >site.yml <<EOF
- hosts: all
  roles:
    - pulp3-postgresql
    - pulp3-workers
    - pulp3-resource-manager
    - pulp3-webserver
EOF
cat >inventory <<EOF
centos-7-pulp-3
fedora-27-pulp-3
fedora-28-pulp-3
EOF
mkdir {group,host}_vars
cat >group_vars/all <<EOF
pulp_secret_key: secret
pulp_default_admin_password: password
EOF
cat >host_vars/fedora-27-pulp-3 <<EOF
ansible_python_interpreter: /usr/bin/python3
EOF
ansible-playbook site.yml --inventory inventory
```

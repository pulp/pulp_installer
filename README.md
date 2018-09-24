ansible-pulp3
=============

Pulp 3 Ansible installer.

The Pulp 3 Ansible installer consists of several roles. Each role installs and
configures a component of Pulp. For example, the `pulp3-postgresql` role
installs and configures PostgreSQL. The roles are not available on Ansible
Galaxy. (This may change in the future.) To run the Pulp 3 Ansible installer,
the [ansible-pulp3](https://github.com/pulp/ansible-pulp3) git repository must
be cloned.

Usage
-----

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

# The current ANXS.postgresql release doesn't support Fedora.
cat >requirements.yml <<EOF
- src: https://github.com/ANXS/postgresql
  version: master
  name: ANXS.postgresql
EOF
ansible-galaxy install -r requirements.yml

ansible-playbook site.yml --inventory inventory
```

Development
-----------

To run the test harness:

1. Install [tox](https://tox.readthedocs.io/en/latest/). This can be done
   through the system package manager or into a virtualenv:

   ```bash
   python3 -m venv ~/.venvs/ansible-pulp3
   pip install --upgrade pip
   pip install tox
   ```
2. Install at least one of the Python interpreters listed in tox.ini. These are
   currently Python 2.7 and 3.6.
3. Install Docker, and add yourself to the group that is authorized to
   administer containers, and log out and back in to make the permissions change
   take effect. The authorized group is typically the "docker" group:

   ```bash
   gpasswd --add "$(whoami)" docker
   ```

   **WARNING:** Anyone added to the docker group is root equivalent. More
   information [here](https://github.com/docker/docker/issues/9976) and
   [here](https://docs.docker.com/engine/security/security/).

   **NOTE:** Docker containers can differ from bare-metal or VM OS installs.
   They can have different packages installed, they can run different kernels,
   and so on.
4. Run `tox`. If you only have a subset of the supported Python interpreters
   available, specify which environments to exercise:

   ```bash
   tox -e py36
   ```

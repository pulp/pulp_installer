Pulp 3 Ansible installer
========================

The Pulp 3 Ansible installer consists of a collection of roles. Each role installs and configures a
component of Pulp. The roles are not currently available on Ansible Galaxy; to run the Pulp 3
Ansible installer, the [ansible-pulp](https://github.com/pulp/ansible-pulp) git repository must
be cloned.

System Requirements
-------------------

The [control node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#control-node)
must have Python 3 and Ansible installed.

The [managed node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#managed-nodes)
must be one of these currently supported operating systems:
* CentOS 7
* Fedora 29 or later

Variables
---------

**Each role documents all the variables that it uses in its own README**. Some variables are
used by multiple roles. In that case, they are be documented in their primary role and mentioned in
the `shared_variables` section the other roles.

**Required Variables:**
Most variables have sane defaults but a few are required. See ``example-use/group_vars/all`` for
the minimal set of required variables.


Ansible Boilerplate
-----------------

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

Using the example playbook
--------------------------

The playbook has external requirements which should be installed from ansible-galaxy.

```
ansible-galaxy install -r requirements.yml
```

You should now be able to run the example playbook.

Some of the roles used in the playbook use root privalages on the managed node, so when prompted,
you will need to provide the password for the managed node user.

```
ansible-playbook example-use/playbook.yml -u <managed_node_username> --ask-become-pass
```

To configure a custom install, you will need to set configuration variables. In the simplest case,
they can be set in the playbook. See the ansible docs for more flexible idiomatic alternatives.


Testing
-------

The tests can be run as they are on travis with **tox**, or they can run with various options using
**molecule** directly.

**Requirements:**
Install Docker, and add yourself to the group that is authorized to
administer containers, and log out and back in to make the permissions change
take effect. The authorized group is typically the "docker" group:

```bash
gpasswd --add "$(whoami)" docker
```

**NOTE:** Docker containers can differ from bare-metal or VM OS installs.
They can have different packages installed, they can run different kernels,
and so on.

**Using Tox:**

1. Install [tox](https://tox.readthedocs.io/en/latest/). This can be done
   through the system package manager or into a virtualenv:

   ```bash
   python3 -m venv ~/.venvs/ansible-pulp
   pip install --upgrade pip
   pip install tox
   ```
2. Install at least one of the Python interpreters listed in tox.ini. These are
   currently Python 2.7 and 3.6.
   **WARNING:** Anyone added to the docker group is root equivalent. More
   information [here](https://github.com/docker/docker/issues/9976) and
   [here](https://docs.docker.com/engine/security/security/).

4. Run `tox`. If you only have a subset of the supported Python interpreters
   available, specify which environments to exercise:

   ```bash
   tox -e py36
   ```

**Using Molecule:**

1. Install [molecule](https://molecule.readthedocs.io/en/latest/). It is recommended that you do so
   with `pip` in a virtualenv.
2. Run molecule commands.

   Test all scenarios on all hosts.
   ```bash
   molecule test --all
   ```

   Test a specific scenario.
   ```bash
   molecule test --scenario-name source
   ```

   Use debug for increased verbosity.
   ```bash
   molecule --debug test --all
   ```

   Create and provision, but don't run tests or destroy.
   ```bash
   molecule converge --all
   ```

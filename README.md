ansible-pulp3
=============

Pulp 3 Ansible installer.

The Pulp 3 Ansible installer consists of several roles. Each role installs and
configures a component of Pulp. For example, the `pulp3-postgresql` role
installs and configures PostgreSQL. The roles are not currently available on
Ansible Galaxy. To run the Pulp 3 Ansible installer, the
[ansible-pulp3](https://github.com/pulp/ansible-pulp3) git repository must
be cloned.

Requirements
------------

The [control node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#control-node)
must have Python 3 and Ansible installed.

The [managed node](https://docs.ansible.com/ansible/2.5/network/getting_started/basic_concepts.html#managed-nodes)
must be one of these currently supported operating systems:
* Fedora 27
* Fedora 28
* CentOS 7

Knowledge of [Ansible](https://www.ansible.com/) is not necessary for the
[Vagrant](https://www.vagrantup.com/) installed, but will be very helpful for
installations that go beyond the default configuration.

Required Variables
------------------

Each role documents its own variables. Most have sane defaults, but a few are required.


User Installation
-----------------

These roles can be used against any managed node and are highly configurable.
Knowledge of [ansible basics](https://docs.ansible.com/ansible/2.5/user_guide/intro_getting_started.html)
will be helpful, but even if you are new to Ansible, this section will get you
started, or you can try the Vagrant installations to bypass the Ansible boilerplate.

First, you will need to configure ssh between your control node and your
managed node. When you can ssh into the managed node without a password, you
are ready to move to the next step.

Next, add the managed node's hostname or ip address to `/etc/ansible/hosts`.

It may be helpful to ensure that Ansible can communicate with the managed node.

```
ansible all -m ping -u <managed_node_username>
```

You should now be able to run the example playbook. The playbook uses `become`
(root), so when prompted, you will need to provide the password for the managed
node user.

```
ansible-galaxy install -r requirements.yml
ansible-playbook user-sandbox.yml -u <managed_node_username> --ask-become-pass -e ansible_python_interpreter=/usr/bin/python3
```

To configure a custom install, you will need to set configuration variables. In
the simplest case, they can be set in the playbook, which is done in our example
playbook, `user-sandbox.yml`. See the ansible docs for more flexible
alternatives.

All configuration options are documented in the README of the roles that use them.


Sandbox Quickstart
------------------

This section provides a fast and simple way to create a Pulp sandbox on a
Vagrant virtual machine that includes the
[pulp_file](https://github.com/pulp/pulp_file) plugin.

First, install some prerequisite packages:

`$ sudo dnf install vagrant ansible vagrant-libvirt vagrant-hostmanager`

After cloning this repository locally, you will need to create a Vagrantfile in
the root of the ansible-pulp3 directory.

`$ cp Vagrantfile.user.example Vagrantfile`

Thats it! Run Vagrant and you will have a Pulp sandbox.

`$ vagrant up`

You can ssh into the guest VM with `vagrant ssh` or you can access the web API
from your host machine. The hostname of the VM is `sandbox.pulp3` and the server
listens on port 80. If you have [httpie](https://httpie.org/) installed, an API
call to the sandbox would look like this:

`$ http --auth admin:password http://sandbox.pulp3/pulp/api/v3/status/`

For more on what you can do with your sandbox, we recommend using the
[pulp_file documentation](https://github.com/pulp/pulp_file/blob/master/README.rst)
next.

To install other plugins, simply add them to the vars in `user-sandbox.yml`. You
can rerun the playbook with `vagrant provision`.

Source Installation:
--------------------

This section will provide a Vagrant machine with editable source installs of
Pulp and the file plugin.

First, you will need to install system requirements. The provided Vagrantfile
Source installs require an additional package, `vagrant-sshfs`, to share files
with your guest virtual machine.

`$ sudo dnf install vagrant ansible vagrant-sshfs vagrant-libvirt vagrant-hostmanager`

You will need to clone the necessary repositories. The provided
`Vagrantfile.source.example` requires that all git repositories are cloned into
a single parent directory.

```
$ git clone https://github.com/pulp/ansible-pulp3.git
$ git clone https://github.com/pulp/pulp.git
$ git clone https://github.com/pulp/pulp_file.git
```

Create your Vagrantfile and use it.

```
$ cp Vagrantfile.source.example Vagrantfile
$ vagrant up
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

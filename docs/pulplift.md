Pulplift
========

This is based on and makes use of the Vagrant based configuration of the
[Forklift](https://github.com/theforeman/forklift) project.
Please see the Forklift documentation for all configuration options available when creating custom
boxes.

Requirements
------------

- Ansible 2.9+
- Vagrant 1.8+
- Vagrant provider plugin (follow [vagrant](
  https://www.vagrantup.com/docs/providers/installation.html) instructions)
  - libvirt and virtualbox supported
- Recommended: [Vagrant sshfs plugin](https://github.com/dustymabe/vagrant-sshfs#install-plugin) if using libvirt
- Enabled virtualization in BIOS

#### Quick install requirements on Fedora

```
sudo dnf install ansible vagrant-libvirt vagrant-sshfs @virtualization
sudo virt-host-validate
```

Setup
-----

Before using Pulplift, ensure that all submodules are updated and in place.

```
git submodule update --init
```

After your git submodules are installed, you can use `vagrant up <box-name>` to create a Pulp
environment.
A list of available boxes including your custom ones can be seen with `vagrant status`.

Setting up a pulp development environment
-----------------------------------------

After you've set up the git submodules as outlined in the Setup section, you will need to
[clone the source code](https://docs.pulpproject.org/en/master/nightly/contributing/dev-setup.html#get-the-source).

If you have any custom configuration options **including plugin choice**,
see "Configuration" section below.

You can now spin up your development environment with:

```
vagrant up pulp3-source-fedora32
```

For more information about the development environment,
please look into the [pulp_devel](https://github.com/pulp/pulp_installer/tree/master/roles/pulp_devel) role.
See also [pulp_installer](https://github.com/pulp/pulp_installer#roles).

Available Boxes
---------------

The aim is to provide every supported OS and major installation type combination for Pulp 3 based
upon what is available from [pulp_installer](https://github.com/pulp/pulp_installer).

#### Base OS Boxes

The base OS boxes, such as `centos7`, can be used to spin-up a clean environment.

```
vagrant up centos7
```

#### Sandbox boxes

Sandbox boxes, such as `pulp3-sandbox-centos7` can be used to do a standard install of Pulp for users.

```
vagrant up pulp3-sandbox-centos7
```

#### Source boxes

Source boxes, such as `pulp3-source-centos7` can be used to do an install of pulp with developer tools & helper scripts/aliases for developers.

The example [configuration](#Configuration) requires that the `pulpcore` git repo directory and plugin git repo directories (e.g. `pulp_file`) exist in folders,
under the same parent folder as `pulplift`, so they can be mounted on the box.

If using libvirt, the [vagrant-sshfs](https://github.com/dustymabe/vagrant-sshfs#install-plugin) plugin must be installed to mount.

```
vagrant up pulp3-source-centos7
```

## Ansible

Any of the `pulp3` labeled boxes will both spin-up and provision the labeled Ansible installation
scenario for Pulp 3.

#### Configuration

Each box uses a playbook appropriate for the type of installation specified in the box name.
Additional ansible variables are defined in `example.user-config.yml` for sandbox installations
and `example.dev-config.yml` for development installations respectively.
If you need to change these variables, **including choosing which plugins to install**,
copy one of these files to **create a local variable file**.
Pulplift will first look for `local.user-config.yml` or `local.dev-config.yml`,
which are not checked into git.

Any of the Ansible variables can be set in this local variable file.
Please see the README of each [pulp_installer](https://github.com/pulp/pulp_installer#roles) role
for more detailed information.

#### Running a playbook directly

You can run an existing or custom playbook directly using `ansible-playbook`.
For example:

```
vagrant up centos7
ansible-playbook -i forklift/inventories/ -l centos7 my-pulp-install.yaml
```

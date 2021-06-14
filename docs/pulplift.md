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
[clone the source code](https://docs.pulpproject.org/en/master/nightly/contributing/dev-setup.html#get-the-source)
in the parent directory of the `pulp_installer` clone.

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

The example [configuration](#configuration) requires that the `pulpcore` git repo directory and plugin git repo directories (e.g. `pulp_file`) exist in folders,
under the same parent folder as `pulp_installer`, as they will be mounted on the box.

If using libvirt, the [vagrant-sshfs](https://github.com/dustymabe/vagrant-sshfs#install-plugin) plugin must be installed to mount.

```
vagrant up pulp3-source-centos7
```

#### FIPS box pair

The following source/development boxes are meant to be run together as a pair:
- pulp2-nightly-pulp3-source-fips-a (Pulp 3 **VM**)
- pulp2-nightly-pulp3-source-fips-b (Pulp 2 **container** that runs **on top** of the "a" VM)


To create or start them, this is the shortest command:
```
vagrant up pulp2-nightly-pulp3-source-fips-a && vagrant up --provider docker pulp2-nightly-pulp3-source-fips-b || vagrant up --provider docker pulp2-nightly-pulp3-source-fips-b
```

You will then do your Pulp 3 development on the A box, which includes the mongo client:
```
vagrant ssh pulp2-nightly-pulp3-source-fips-a
```

To destroy them, you must destroy b 1st, and you may need to force it:
```
vagrant destroy --force pulp2-nightly-pulp3-source-fips-b && vagrant destroy --force pulp2-nightly-pulp3-source-fips-a
```

NOTE: We repeat the command to work around a net-ssh ["poll_next_packet' padding error"](https://github.com/hashicorp/vagrant/issues/3951#issuecomment-73057077) that is triggered about 50% of the time, the 1st time it is run only.

If you ever run into a situation where Vagrant cannot enumerate the VMs at all (`vagrant status`) because it cannot talk to the docker host (a), run one of the following:
- vagrant up pulp2-nightly-pulp3-source-fips-a
- vagrant destroy --force pulp2-nightly-pulp3-source-fips-b

If using libvirt, the [vagrant-sshfs](https://github.com/dustymabe/vagrant-sshfs#install-plugin) plugin must be installed to mount.

NOTE: FIPS is not supported by Pulp. These FIPS boxes, like all the other boxes with "fips" in their
name, are provided for those who would like test their plugins in FIPS environment and
potentially apply their own FIPS patches to Django.

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
which are not checked into git. To overwrite those settings for an individual one of your vagrant
instances, you can provide a `local.<hostname>-config.yml`.

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

## Configuring Vagrant to run on a HDD

Vagrant boxes that are libvirt-based use storage-pool to for VMs that are created. So to get a
libvirt based pulp_installer box running on a HDD disk you need to:

1. Create a new storage pool on your HDD
2. Configure Vagrant to use that storage pool

### Creating a new storage pool on your spinny disk

1. Have a mounted, HDD, e.g. mine is mounted at: `/run/media/bmbouter/2TB\ External/`
2. I wanted to have the VMs use a specific directory, so I manually created `/run/media/bmbouter/2TB\ External/slow_pool`.
4. Use the interactive `virsh` tool to create a pool, e.g. `pool-define-as slow_pool --type dir --target /run/media/bmbouter/2TB\ External/slow_pool`
5. Start the pool using `virsh` to run `pool-start slow_pool`.
6. You could also mark the pool to auto-start with `pool-autostart slow_pool`.

Now you have the `slow_pool`.

### Give Vagrant the `storage_pool_name` option

For pulp_installer this can only be done on the vagrant "box definition" itself. The
`local.dev-config.yml` and `local.user-config.yml` files only specifies Ansible variables. These are
not the same as Vagrant box definitions, which for [the pulp_installer live here](https://github.com/pulp/pulp_installer/tree/master/vagrant/boxes.d)

This is documentation for libvirt backends, and we're going to be using the `storage_pool_name`
which is an option for `libvirt_options`. The docs referring to this are [here](https://github.com/vagrant-libvirt/vagrant-libvirt#provider-options).

In my case I wanted to modify the `pulp2-nightly-pulp3-source-centos7` box, so I applied this diff:

```
diff --git a/vagrant/boxes.d/30-source.yaml b/vagrant/boxes.d/30-source.yaml
index 72b70b4..68876cc 100644
--- a/vagrant/boxes.d/30-source.yaml
+++ b/vagrant/boxes.d/30-source.yaml
@@ -40,6 +40,8 @@ pulp2-nightly-pulp3-source-centos7:
     reverse: False
   memory: 10500
   cpus: 4
+  libvirt_options:
+    storage_pool_name: "slow_pool"
   ansible:
     playbook:
       - "pulp-ci/ci/ansible/pulp_server.yaml"
```

Then I ran `vagrant up pulp2-nightly-pulp3-source-centos7`. I knew it worked because it showed me:

```
<snip>
==> pulp2-nightly-pulp3-source-centos7:  -- Storage pool:      slow_pool
==> pulp2-nightly-pulp3-source-centos7:  -- Image:             /run/media/bmbouter/2TB External/slow_pool/pulp_installer_pulp2-nightly-pulp3-source-centos7.img (128G)
<snip>
```

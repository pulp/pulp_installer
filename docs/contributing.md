Contributing
============

Pull Request Checklist
------------------------
1. Make sure your change does not break idempotency tests. See [Testing](#Testing)
(or let CI run the tests for you if you are certain it is idempotent.)
If a task cannot be made idempotent, add the tag [molecule-idempotence-notest](https://github.com/ansible-community/molecule/issues/816#issuecomment-573319053).
2. Unless a change is small or doesn't affect users, [create an issue on GitHub](https://github.com/pulp/pulp_installer/issues).
3. Add [a changelog update.](https://docs.pulpproject.org/contributing/git.html#changelog-update)
4. Write an excellent [Commit Message.](https://docs.pulpproject.org/contributing/git.html#commit-message)
Make sure you reference and link to the issue.
5. Push your branch to your fork and open a [Pull request across forks](https://help.github.com/articles/creating-a-pull-request-from-a-fork/).
6. Add GitHub labels as appropriate.

Testing
-------

The tests can be run as they are on GitHub Actions with **tox**, or they can run with various options
using **molecule** directly.

### Requirements

Install Docker, and add yourself to the group that is authorized to
administer containers, and log out and back in to make the permissions change
take effect. The authorized group is typically the "docker" group:

```bash
gpasswd --add "$(whoami)" docker
```

**NOTE:** Docker containers can differ from bare-metal or VM OS installs.
They can have different packages installed, they can run different kernels,
and so on.

### Using Molecule

1. Install [molecule](https://molecule.readthedocs.io/en/latest/),
molecule-docker, ansible
and [ansible-lint](https://docs.ansible.com/ansible-lint/).
It is recommended that you do so with `pip` in a virtualenv for Python 3.6+.

2. Install collection dependencies

`ansible-galaxy collection install -r ./requirements.yml`

3. Run molecule commands.

   Test the default scenario, release-static, on all hosts (linux distros.)
   ```bash
   molecule test
   ```

   Test a specific scenario.
   ```bash
   molecule test --scenario-name source
   ```

   Test all scenarios on all hosts.
   ```bash
   molecule test --all
   ```

   Use debug for increased verbosity.
   ```bash
   molecule --debug test
   ```

   Create and provision, but don't run tests or destroy.
   ```bash
   molecule create

   ```
   Run the main test phase "converge" after creating and provisioning.
   ```bash
   molecule converge
   ```

### Explanation of Different Molecule Scenarios

The molecule scenarios have names like `release-static`, which we will refer to as
"prefix-suffix".

There is a 3 by 3 matrix of them.

The prefixes are:

1. `release` - Install stable release from PyPI
1. `source` - Install from git checkout. Different codepaths; preflight check does not exist.
1. `packages` - Install from distro (RPM) packages. Even more different codepaths; compatibility
   checks (preflight) is the job of the repo maintainer.

The suffixes are:

1. `static` - Statically specify the roles in the "roles:" syntax in the main playbook, such as in
   the example playbooks.
1. `cluster` - Runs as few roles as possible per host, creating a pulp cluster, rather than
   a set of independent pulp hosts. Catches any issues.
   Also, run roles 1 at a time via `include_role:` under `tasks:` in the main playbook.
   Catches undeclared dependencies between roles, and other "dynamic" include errors. This covers use
   cases such as users running a 3rd party role, setting vars, and later running our role.
1. `upgrade` - Upgrade an existing Pulp 3.y container, to test upgrading Pulp 3.y. Roles are applied
   statically. Depends on said containers existing on a registry, and having been built manually
   (See [instructions below)](#creating-molecule-upgrade-test-containers))

`release-static` is symlinked to `default`, so that commands like `molecule test` will use it.

There are other (intentional) differences between tests:

1. `static` - These include using unix sockets for the webserver to connect to pulp-api
   & pulp-content. The remainder use TCP connections (`upgrade` because that's what older installs
   only did, `cluster` because containers communicate via TCP.)
1. The `release-upgrade` scenario uses its own `converge.yml` playbook instead of the default one
   used by all other scenarios. This playbook upgrades a Pulp installation multiple times to ensure
   that all upgrade scenarios work correctly.
1. The `source-static` scenario defines paths different than the default for the following variables:
   `pulp_media_root`, `pulp_settings.working_directory`, `pulp_user_home`, `pulp_install_dir`,
   `pulp_config_dir` and `developer_user_home`.

In order for `cluster` scenarios to work on your local system, you must do the following to enable
container networking:
1. Run `firewall-cmd --zone=public --add-masquerade --permanent` (assuming your firewall zone is
   `public`).
1. Run
   `firewall-cmd --permanent --zone=public --add-rich-rule='rule family=ipv4 source address=172.27.0.0/16 accept'`
   (assuming your firewall zone is `public`).
1. Create /etc/sysctl.d/10-allow_docker_networking.conf with and reboot:
```
net.bridge.bridge-nf-call-iptables=0
net.bridge.bridge-nf-call-arptables=0
net.bridge.bridge-nf-call-ip6tables=0
```

To test both webserver solutions we testing `apache` as webserver with

* packages-cluster
* source-cluster
* release-static

All others scenarios use `nginx` as a webserver.

Docs Testing
------------

Cross-platform:
```bash
pip install mkdocs pymdown-extensions mkdocs-material mike mkdocs-git-revision-date-plugin
```

Then:
```bash
mkdocs serve
```
Click the link it outputs. As you save changes to files modified in your editor,
the browser will automatically show the new content.

NFS & SELinux testing
---------------------
Here are example commands for testing the functionality prescribed for the variable
[`pulp_selinux_remount_data_dir`](helper_roles/pulp_common):
```bash
vagrant up --no-destroy-on-error pulp3-sandbox-centos9-stream
(hit ctrl-c while ansible-galaxy is running, or early on in the ansible run)
vagrant ssh pulp3-sandbox-centos9-stream
sudo -i
dnf install -y nfs-utils
systemctl enable --now nfs-server.service
mkdir -p /data/var/lib/pulp/pulpcore_static/
mkdir -p /var/lib/pulp/pulpcore_static/
echo '/data/var/lib/pulp 127.0.0.1(rw,no_root_squash)' >> /etc/exports
exportfs -a
echo '127.0.0.1:/data/var/lib/pulp /var/lib/pulp nfs defaults,_netdev,nosharecache 0 0' >> /etc/fstab
echo '127.0.0.1:/data/var/lib/pulp/pulpcore_static /var/lib/pulp/pulpcore_static,nosharecache nfs defaults,_netdev,context="system_u:object_r:httpd_sys_content_rw_t:s0" 0 0' >> /etc/fstab
mount -a
exit
exit
vagrant provision pulp3-sandbox-centos9-stream
```


Creating Molecule Upgrade Test Containers
-----------------------------------------

1. Identify a version from 3.14 or older (because the release-upgrade tests 1st test upgrading to
   3.14 before the current version. This should be revisited in the future.)
2. Identify how you will build the old version. Preferably using the old version of the installer.
   But if necessary, modifying the version variables with the current installer.
3. Modify molecule/release-static/group_vars (or host_vars) so that the webserver is nginx rather
   than apache, and so that pulp_container is not installed. Also modify the version variables
   (including `pulpcore_version`) if need be. Install release versions of pulpcore and plugins.
4. `molecule create && molecule converge`
5. If that failed, be prepared to put workarounds on the branch. Such as modifying `prereq_pip_packages`.
5. `docker exec -it <container-name> /bin/bash`
6. `dnf clean all`
7. `rm -rf /var/lib/pulp/.cache`
8. `exit`
9. `docker commit <container-name <tag-name>` with a tag like
   "quay.io/pulp/pulp_installer-pip-ci-f36:3.13.0"
10. Modify molecule.yml for release-upgrade and source-upgrade (or packages-upgrade)
11. Test the image locally (molecule create -s release-upgrade && molecule converge -s release-upgrade)
12. `docker push <tag-name>`
13. If this is the 1st image of a new distro, go to https://quay.io/organization/pulp, set the descritpion
    of the repo based on existing ones, and set the repo to public.
14. Create a PR.

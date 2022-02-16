Contributing
============

Pull Request Checklist
------------------------
1. Make sure your change does not break idempotency tests. See [Testing](#Testing)
(or let CI run the tests for you if you are certain it is idempotent.)
If a task cannot be made idempotent, add the tag [molecule-idempotence-notest](https://github.com/ansible-community/molecule/issues/816#issuecomment-573319053).
2. Unless a change is small or doesn't affect users, create an issue on
https://github.com/pulp/pulp_installer/issues . Set the Category to "Installer".
3. Add [a changelog update.](https://docs.pulpproject.org/contributing/git.html#changelog-update)
4. Write an excellent [Commit Message.](https://docs.pulpproject.org/contributing/git.html#commit-message)
Make sure you reference and link to the issue.
5. Push your branch to your fork and open a [Pull request across forks.](https://help.github.com/articles/creating-a-pull-request-from-a-fork/)
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

2. Run molecule commands.

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
1. `dynamic` - Run roles 1 at a time via `include_role:` under `tasks:` in the main playbook.
   Catches undeclared dependencies between roles, and other dynamic include errors. Covers use cases
   such as users running a 3rd party role, setting vars, and later running our role. Later
   on, will probably be replaced with installing pulp against multiple containers, each 1 role.
1. `upgrade` - Upgrade an existing Pulp 3.y container, to test upgrading Pulp 3.y. Roles are applied
   statically. Depends on said containers existing on a registry, and having been built manually
   (using `docker commit` from molecule.)

`release-static` is symlinked to `default`, so that commands like `molecule test` will use it.

There are other (intentional) differences between tests:

1. `static` - These include using unix sockets for the webserver to connect to pulp-api
   & pulp-content. The remainder use TCP connections (`upgrade` because that's what older installs
   only did, `dynamic` because they will become containers soon anyway to test cluster installs.)
1. `dynamic` - Due to a limitation of Ansible 2.8 with collections, these are not tested with
   Ansible 2.8.
1. The `release-upgrade` scenario uses its own `converge.yml` playbook instead of the default one
   used by all other scenarios. This playbook upgrades a Pulp installation multiple times to ensure
   that all upgrade scenarios work correctly.
1. The `source-static` scenario defines paths different than the default for the following variables:
   `pulp_media_root`, `pulp_cache_dir`, `pulp_user_home`, `pulp_install_dir`, `pulp_config_dir` and
   `developer_user_home`.

To test both webserver solutions we testing `apache` as webserver with

* package-dynamic
* source-dynamic
* release-static

All others scenarios use `nginx` as a webserver.

Docs Testing
------------

On Fedora:
```
sudo dnf install mkdocs python3-pymdown-extensions
```

Cross-platform:
```
pip install mkdocs pymdown-extensions
```

Then:
```
`mkdocs serve`
```
Click the link it outputs. As you save changes to files modified in your editor,
the browser will automatically show the new content.

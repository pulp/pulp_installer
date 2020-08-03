Contributing
============

Pull Request Checklist
------------------------
1. Make sure your change does not break idempotency tests. See [Testing](#Testing)
(or let CI run the tests for you if you are certain it is idempotent.)
If a task cannot be made idempotent, add the tag [molecule-idempotence-notest](https://github.com/ansible-community/molecule/issues/816#issuecomment-573319053).
2. Unless a change is small or doesn't affect users, create an issue on
https://pulp.plan.io/projects/pulp . Set the Category to "Installer".
3. Add [a changelog update.](https://docs.pulpproject.org/contributing/git.html#changelog-update)
4. Write an excellent [Commit Message.](https://docs.pulpproject.org/contributing/git.html#commit-message)
Make sure you reference and link to the issue.
5. Push your branch to your fork and open a [Pull request across forks.](https://help.github.com/articles/creating-a-pull-request-from-a-fork/)
6. Add GitHub labels as appropriate.

Testing
-------

The tests can be run as they are on GitHub Actions with **make** and **tox**, or they can run with various options
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

### Using Tox

1. Install [tox](https://tox.readthedocs.io/en/latest/). This can be done
   through the system package manager or into a virtualenv:

   ```bash
   python3 -m venv ~/.venvs/pulp_installer
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
   make test TOX_ENV=py36-ansible28-release-static
   ```

### Using Molecule

1. Install [molecule](https://molecule.readthedocs.io/en/latest/),
and [ansible-lint](https://docs.ansible.com/ansible-lint/).
It is recommended that you do so with `pip` in a virtualenv.

2. Prepare collection.

   Install the collection into the test environment.
   (You need to repeat this step whenever you changed a file.)
   ```bash
   make install
   ```

3. Run molecule commands.

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

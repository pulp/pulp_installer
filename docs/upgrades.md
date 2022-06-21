Upgrades and Installing Particular Versions
===========================================

When installing Pulp, there are 3 software components whose versions you should be mindful of:

1. pulp_installer
1. pulpcore
1. 1 or more plugins

If all you want to do is install Pulp and upgrade it to the very latest version in the future,
you may not need to specify any versions. However, it is recommended to specify versions at the time
of installation for 2 reasons

* Handling a situation where not all your plugins compatible with the latest pulpcore version.
* Doing updates/upgrade in the future in a controlled manner.

There are 3 sets of **workflows** below. Each workflow supports installations and upgrades, the latter
2 support updates and handling plugin compatibility:

* ["Latest Version with Minimal Effort"](#latest-version-with-minimal-effort)
* ["Specifying Minor Releases of Pulpcore and Plugins"](#specifying-minor-releases-of-pulpcore-and-plugins)
* ["Specifying Exact Versions with Reproducibility"](#specifying-exact-versions-with-reproducibility)

### Explanation of plugin version compatibility with Pulpcore

Pulp 3 has a plugin architecture so that new content types and features can be added by the
larger community. However, both pulpcore & plugins are installed by the installer using `pip`, which has limited
dependency resolution. Plugins release at their own lifecycles. Thus in the worst case scenario, the
latest release of plugin pulp_juicy could depend on the current minor version (e.g., 3.10.z) of
pulpcore, while the latest release of pulp_sugary could depend on only older versions of pulpcore
(e.g., 3.8.z or 3.9.z). But if pulp_juicy were to also support 3.9.z, then the installer can handle this
use case with a workflow listed below.

In order to avoid breaking multiple plugins for the sake of one plugin, and to avoid breaking existing
installations, upgrading a plugin will not cause pulpcore to be updated as a dependency. Similarly,
if there is an attempt to update a plugin to a version that is incompatible with pulpcore, the installer
will fail and exit. The installer does a compatibility check early in the installation to prevent Pulp
from being installed or upgraded to an incompatible set of versions.

Thus you, yourself, must research plugin compatibility with the pulpcore version whenever you are
installing one or more plugins. With each plugin release, the plugin compatibility is announced as
part of the release announcement and included in the documentation for the specific plugin.


### Latest Version with Minimal Effort:

#### **Initial installation:**

1. [Make sure](https://galaxy.ansible.com/pulp/pulp_installer) you are running the latest version of the installer, which
   installs pulpcore's latest minor (3.y) release.
1. Confirm that all the latest stable releases of your desired plugins are compatible with
   pulpcore's latest version, such as by reading the release announcement email thread for
   pulpcore's latest version, reading the plugins' README, or reading their `setup.py`.
1. If they are not all compatible yet, follow the latter section
   ["Latest patch releases for minor releases of pulpcore and plugins"](#latest-patch-releases-for-minor-releases-of-pulpcore-and-plugins) instead.
1. Set `pulp_install_plugins` with each plugin name listed as a key, with no value listed.
1. Run `pulp_installer`.
1. Make sure to save your variables/playbook for later usage.

Command to install pulp_installer's latest version:

```bash
ansible-galaxy collection install --force pulp.pulp_installer
```

Example `pulp_install_plugins`:

```yaml
  vars:
    pulp_install_plugins:
      pulp-container:
      pulp-file:
      pulp-rpm:
```

#### **Upgrading your installation to the latest version:**

1. [Observe](https://galaxy.ansible.com/pulp/pulp_installer) what is the latest version of `pulp_installer`,
   its minor release (3.y) will correspond to the minor release of pulpcore it installs.
1. Confirm that all the latest stable releases of all **currently installed** plugins are compatible
   with pulpcore's latest version, such as by reading the release announcement email thread for pulpcore's
   latest version, reading the plugins' README files, or reading their setup.py.
1. If they are not all compatible yet, **wait** for the plugins to be updated for
   compatibility, or follow the latter section ["Latest patch releases for minor releases of pulpcore and plugins"](#latest-patch-releases-for-minor-releases-of-pulpcore-and-plugins) instead.
1. Set `pulpcore_update` to `true`. (This will ensure that even if you are on the same minor (3.y) release as
   initial installation, the latest patch release (3.y.z) will be installed.)
1. Set `pulp_install_plugins` with each plugin name listed as a key, and with each plugin having a key under it
   called `upgrade`, with the value set to `true`.
1. Update/upgrade your installer to the latest version (3.y.z) of the 3.y minor release.
1. Re-run `pulp_installer`.
1. Make sure to save your variables/playbook for later usage.

Command to upgrade pulp_installer to its latest version:

```bash
ansible-galaxy collection install --force pulp.pulp_installer
```

Example `pulp_install_plugins`:

```yaml
  vars:
    pulpcore_update: true
    pulp_install_plugins:
      pulp-container:
        upgrade: true
      pulp-file:
        upgrade: true
      pulp-rpm:
        upgrade: true
```

### Specifying Minor Releases of Pulpcore and Plugins

#### **Initial installation:**

1. [Observe](https://galaxy.ansible.com/pulp/pulp_installer) what is the latest version of `pulp_installer`,
   its minor release (3.y) will correspond to the minor release of pulpcore it installs.
   We will assume they are minor version `3.9`.
1. Confirm that all the latest stable releases of your desired plugins are compatible with
   pulpcore's latest version, such as by reading the release announcement email thread for
   pulpcore's latest version, reading the plugins' README, or reading their `setup.py`.
1. If they are not all compatible yet, try researching the **previous** minor release (`3.9`) of the installer
   and pulpcore. Confirm that there exist stable releases of your desired plugins that are compatible
   with said release. If there are none, try the minor release before that (`3.8`) and repeat.
1. Once a compatible pulpcore version and plugin versions are found, Set `pulp_install_plugins`
   with each plugin name listed as a key, and with each plugin having a key under it called `version` set
   to the minor version (3.y) as the value (with quotes).
1. Upgrade or downgrade your installer to the latest version (3.y.z) of the pulpcore minor release (3.y) you
   need. (The installer's minor version will control what minor version of pulpcore gets installed.)
1. Run `pulp_installer`.
1. Make sure to save your variables/playbook for later usage.

Command to install pulp_installer's latest version:

```bash
ansible-galaxy collection install --force pulp.pulp_installer
```

Example command to install a specific version of pulp_installer:

```bash
ansible-galaxy collection install --force pulp.pulp_installer:3.9.1
```

Example `pulp_install_plugins`:

```yaml
  vars:
    pulp_install_plugins:
      pulp-container:
        version: "2.8"
      pulp-file:
        version: "1.9"
      pulp-rpm:
        version: "3.15"
```

#### **Updating your installation:**

    Note: These are update instructions, not upgrade instructions. They will keep you on the same pulpcore
    minor version (3.y) as initially installed.

1. [Update](https://galaxy.ansible.com/pulp/pulp_installer) `pulp_installer` to the latest patch release (3.y.z)
   within the minor release (3.y) that was used for the initial installation.
1. Set `pulpcore_update` to `true`.
1. Set `pulp_install_plugins` with each **currently installed** plugin's name listed as a key.
   For each plugin add a key under it
   called `version` set to the currently installed `x.y` plugin version. Add a key under the plugin name
   called `upgrade` set to
   the value `true`. (This combination will update the plugin to the latest patch release.)
1. Re-run `pulp_installer`.
1. Make sure to save your variables/playbook for later usage.

Example command to update to a specific version of pulp_installer:

```bash
ansible-galaxy collection install --force pulp.pulp_installer:3.9.2
```

Example `pulp_install_plugins`:

```yaml
  vars:
    pulpcore_update: true
    pulp_install_plugins:
      pulp-container:
        version: "2.8"
        upgrade: true
      pulp-file:
        version: "1.9"
        upgrade: true
      pulp-rpm:
        version: "3.15"
        upgrade: true
```

#### **Upgrading your installation to a specific minor release:**

1. [Observe](https://galaxy.ansible.com/pulp/pulp_installer) what is the latest version of `pulp_installer`,
   its minor release (3.y) will correspond to the minor release of pulpcore it installs.
   We will assume they are minor version `3.10`.
   (Note: Even if there is no upgrade, you can still upgrade your plugins.)
1. Confirm that all the latest stable releases of **currently installed** plugins are compatible
   with pulpcore's latest version, such as by reading the release announcement email thread for
   pulpcore's latest version, reading the plugins' README files, or reading their `setup.py`.
1. If they are not all compatible yet, try researching the **previous** minor release (`3.9`) of the installer
   and pulpcore. Confirm that there exist stable releases of your desired plugins that are compatible
   with said release. If there are none, try the minor release before that (`3.8`) and repeat.
1. Once a compatible pulpcore version and plugin versions are found, Set `pulp_install_plugins` with
   each **currently installed** plugin's name listed as a key,
   and with each plugin having a key under it called `version` set to
   the **new** minor version as the value (with quotes). Add a key under the plugin name called `upgrade` set to
   the value `true`. (This combination will update the plugin to the latest patch release if no upgrade
   is necessary.)
1. Update or downgrade your installer to the latest version (3.y.z) of the pulpcore minor release (3.y) you
   need. (The installer's minor version will control what minor version of pulpcore gets installed.)
1. Set `pulpcore_update` to `true` (this is merely for performing an update of pulpcore, in case its minor
   branch is not changing.)


Example command to upgrade to a specific version of pulp_installer:

```bash
ansible-galaxy collection install --force pulp.pulp_installer:3.10.1
```

Example `pulp_install_plugins`:

```yaml
  vars:
    pulpcore_update: true
    pulp_install_plugins:
      pulp-container:
        version: "2.9"
        upgrade: true
      pulp-file:
        version: "1.10"
        upgrade: true
      pulp-rpm:
        version: "3.16"
        upgrade: true
```

> Note: It is often possible to upgrade plugins without upgrading pulpcore. You can perform this
  by keeping pulp_installer on the same minor branch, setting `pulpcore_update: true`, and raising the
  `version` variables.

### Specifying Exact Versions with Reproducibility:

#### **Initial installation:**

1. [Observe](https://galaxy.ansible.com/pulp/pulp_installer) what is the latest version of `pulp_installer`,
   its minor release (3.y) will correspond to the minor release of pulpcore it installs.
   We will assume they are minor version `3.9`.
1. Observe what the latest release of `pulpcore` is on
   [PyPI](https://pypi.org/project/pulpcore/#history). You will presumably specify this version. We
   will assume it is `3.9.9"`
1. Confirm that all the latest stable releases of your desired plugins are compatible with
   pulpcore's latest version, such as by reading the release announcement email thread for
   pulpcore's latest version, reading the plugins' README, or reading their `setup.py`.
1. If they are not all compatible yet, try researching the **previous** minor release (`3.9`) of the
   installer and pulpcore. Confirm that there exist stable releases of your desired plugins that are compatible
   with said release. If there are none, try the minor release before that (`3.8`) and repeat.
1. Once a compatible pulpcore version and plugin versions are found, Set `pulp_install_plugins` with
   each **currently installed** plugin's name listed as a key,
   and with each plugin having a key under it called `version` set to
   the version as the value (with quotes).
1. Also set `pulpcore_version` to the 3.y.z version of pulpcore (with quotes).
1. Update or downgrade your installer to the latest version (3.y.z) of the minor release (3.y) you
   need. It must be the same minor version as `pulpcore_version`.
1. Run `pulp_installer`
1. Make sure to save your variables/playbook for later usage.

Example command to install a specific version of pulp_installer:

```bash
ansible-galaxy collection install --force pulp.pulp_installer:3.9.1
```

Example `pulp_install_plugins` (with bogus version values):

```yaml
  vars:
    pulpcore_version: "3.9.9"
    pulp_install_plugins:
      pulp-container:
         version: "4.5.6"
      pulp-file:
         version: "5.6.7"
      pulp-rpm:
         version: "6.7.8"
```


#### **Upgrading your installation to a specific patch:**

> Note: These instructions can also be used for updates.

1. [Observe](https://galaxy.ansible.com/pulp/pulp_installer) what is the latest version of `pulp_installer`,
   its minor release (3.y) will correspond to the minor release of pulpcore it installs.
   We will assume they are minor version `3.10`.
   (Note: Even if there is no upgrade, you can still upgrade your plugins.)
1. Observe what the latest release of `pulpcore` is on
   [PyPI](https://pypi.org/project/pulpcore/#history). You will presumably specify this version. We will assume
   it is `3.10.10"`
1. Confirm that all the latest stable releases of **currently installed** plugins are compatible
   with pulpcore's latest version, such as by reading the release announcement email thread for
   pulpcore's latest version, reading the plugins' README files, or reading their `setup.py`.
 If they are not all compatible yet, try researching the **previous** minor release (`3.9`) of the
   installer and pulpcore. Confirm that there exist stable releases of your desired plugins that are compatible
   with said release. If there are none, try the minor release before that (`3.8`) and
   repeat. (But do not try to downgrade pulpcore to an older version than you have installed.)
1. Once a compatible pulpcore version and plugin versions are found, Set `pulp_install_plugins` with
   each **currently installed** plugin's name listed as a key,
   and with each plugin having a key under it called `version`
   set to the **new** version as the value (with quotes).
1. Also set `pulpcore_version` to the  **new** 3.y.z version of pulpcore (with quotes).
1. Update/upgrade or downgrade your installer to the latest version (3.y.z) of the minor release (3.y) you
   need. It must be the same minor version as `pulpcore_version`.
1. Make sure to save your variables/playbook for later usage.

Example command to update/upgrade to a specific version of pulp_installer:

```bash
ansible-galaxy collection install --force pulp.pulp_installer:3.10.1
```

Example `pulp_install_plugins` (with bogus version values):

```yaml
  vars:
    pulpcore_version: "3.10.10"
    pulp_install_plugins:
      pulp-container:
         version: "5.6.7"
      pulp-file:
         version: "6.7.8"
      pulp-rpm:
         version: "7.8.9"
```

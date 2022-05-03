pulp_repos
==========

Role to enable repositories needed to install pulp. It can be disabled if user already have the repositories enabled.

    This role is meant to be called by `include_role` with specific variable.

Requirements
------------

All covered by ansible.

Role Variables
--------------

With its defaults.

* `pulp_repos_enable`: Effectively can disable enablement of all repositories mentioned below.
  Defaults to `True`.

* `pulp_repos_centos_powertools_repo_enable`: to enable CentOS 8 PowerTools repository (defaults to `True`)
* `pulp_repos_epel_enable`: to enable EPEL repository (defaults to `True`)
* `pulp_repos_rhel_codeready_enable`: to enable RHEL8 CodeReady repository (defaults to `True`)
* `pulp_repos_rhel_optional_enable`: to enable RHEL7 Optional repository (defaults to `True`)
* `pulp_rhel_pulpcore_repo_enable`: to add the RHEL/CentOS Pulpcore repo to the system (defaults to `True`).
* `pulp_rhel_scl_repo_enable`: to enable SCL repository (defaults to `True`).

* `pulp_rhel_codeready_repo`: List of possible names for rhel8+ CodeReady Builder repo
  to enable. Once it is found, no further names are attempted.
  Defaults to ["codeready-builder-for-rhel-8-x86_64-rpms", "rhui-codeready-builder-for-rhel-8-rhui-rpms", "codeready-builder-for-rhel-8-rhui-rpms"]
  Only affects RHEL8+.
* `epel_release_packages`: List of strings (package names, URLs) to pass to
  `yum install` to ensure that "epel-release" is installed.
  Once the 1st string is found to be installed by yum, no further strings are
  attempted.
  Also accepts a single string or empty string.
  Only affects CentOS/RHEL.
* `rhel7_optional_repo`: List of possible names for the rhel7 optional repo
  to enable. Once the 1st name is enabled (or found to already be enabled),
  no further names are attempted.
  Defaults to  ["rhui-rhel-7-server-rhui-optional-rpms", "rhel-7-server-optional-rpms", "rhel-7-workstation-optional-rpms"]
  Also accepts a single string or empty string.
  Only affects RHEL7 (RHEL8 no longer has an optional repo.)

Advenced Role Variables
-----------------------

These variables corresponding to role repository variables above when is called by another role.

* `__pulp_repos_centos_powertools_repo_enable_default`: Defaults to `False`
* `__pulp_repos_epel_enable_default`: Defaults to `False`
* `__pulp_repos_rhel_codeready_enable_default`: Default to `False`
* `__pulp_repos_rhel_optional_enable_default`: Defaults to `False`
* `__pulp_rhel_pulpcore_repo_enable_default`: Defaults to `False`
* `__pulp_rhel_scl_repo_enable_default`: Defaults to `False`

Shared Variables
----------------
* `pulp_install_source`: If set to `packages`, and pulp_rhel_pulpcore_repo_enable==true, Add the
  pulpcore repo to the system.

### Example

  ```
  - name: Enable EPEL repository needed by Pulp
    include_role:
      name: pulp_repos
    vars:
      __pulp_repos_epel_enable_default: True
  ```

Example Usage
-------------

If you want to install Pulp on a device with EPEL repository already enabled, you don't want to enable it second time. 
In this case it is enough just put line bellow into your `config.yml`.

    pulp_repos_epel_requested: False

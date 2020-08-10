Getting started
===============

The Pulp 3 Ansible installer is a collection of roles to install or upgrade Pulp 3 hosted on galaxy:
[https://galaxy.ansible.com/pulp/pulp_installer](https://galaxy.ansible.com/pulp/pulp_installer)

Installation
------------
The recommended installation is from ansible-galaxy:

```
ansible-galaxy collection install pulp.pulp_installer
```

Using the example playbook
--------------------------

Some of the roles used in the playbook use root privileges on the managed node, so when prompted,
you will need to provide the password for the managed node user.

```
ansible-playbook playbooks/example-use/playbook.yml -u <managed_node_username> --ask-become-pass
```

<script id="asciicast-335159" src="https://asciinema.org/a/335159.js" async data-autoplay="true" data-speed="2"></script>

To configure a custom installation, you will need to set configuration variables. In the simplest case,
they can be set in the playbook. See the Ansible docs for more flexible idiomatic alternatives.


Example Playbook for Installing Plugins
---------------------------------------
As an example, we are going to write a playbook for installing `pulp_container` and `pulp_rpm`.
You can learn more about the variables on the [roles section](https://pulp-installer.readthedocs.io/en/latest/roles/pulp/#role-variables)

1 -  Install the `pulp_installer` collection:
```
ansible-galaxy collection install pulp.pulp_installer
```

2 -  Install the `geerlingguy.postgresql` role:
```
ansible-galaxy install geerlingguy.postgresql
```

3 - Write the following playbook:
```
vim install.yml
```


```yaml
---
- hosts: all
  vars:
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "https://{{ ansible_fqdn }}"
    pulp_default_admin_password: << YOUR PASSWORD HERE >>
    pulp_install_plugins:
      # galaxy-ng: {}
      # pulp-ansible: {}
      # pulp-certguard: {}
      pulp-container: {}
      # pulp-cookbook: {}
      # pulp-deb: {}
      # pulp-file: {}
      # pulp-gem: {}
      # pulp-maven: {}
      # pulp-npm: {}
      # pulp-python: {}
      pulp-rpm: {}
  roles:
    - pulp.pulp_installer.pulp_all_services
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```
4 - Run the playbook:
```
ansible-playbook install.yml -u <managed_node_username> --ask-become-pass
```
<script id="asciicast-335829" src="https://asciinema.org/a/335829.js" async data-autoplay="true" data-speed="2"></script>

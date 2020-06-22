Getting started
===============

Pulp 3 Ansible installer is a collection of roles to install or upgrade Pulp 3 hosted on galaxy:
[https://galaxy.ansible.com/pulp/pulp_installer](https://galaxy.ansible.com/pulp/pulp_installer)

Some plugins may require a prereq role, if so, you can find the prereq roles under pulp user here:
[https://galaxy.ansible.com/pulp](https://galaxy.ansible.com/pulp)


Requirements
------------
The collection requires [geerlingguy.postgresql](https://galaxy.ansible.com/geerlingguy/postgresql) role,
which should be installed from ansible-galaxy.

```
ansible-galaxy install geerlingguy.postgresql
```

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

To configure a custom install, you will need to set configuration variables. In the simplest case,
they can be set in the playbook. See the ansible docs for more flexible idiomatic alternatives.


My first playbook
-----------------
As an example, we are going to write a playbook for installing `pulp_container` and `pulp_rpm`.
You can learn more about the variables on the [roles section](https://pulp-installer.readthedocs.io/en/latest/roles/pulp/#role-variables)

1 -  Installing pulp_installer collection:
```
ansible-galaxy collection install pulp.pulp_installer
```

2 -  Installing geerlingguy.postgresql role:
```
ansible-galaxy install geerlingguy.postgresql
```

3 - Writing the playbook (Example of playbook below):
```
vim install.yml
```


```yaml
---
- hosts: all
  vars:
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "http://{{ ansible_fqdn }}"
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
4 - Running the playbook:
```
ansible-playbook install.yml -u <managed_node_username> --ask-become-pass
```
<script id="asciicast-335829" src="https://asciinema.org/a/335829.js" async data-autoplay="true" data-speed="2"></script>

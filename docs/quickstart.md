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
      # pulp-2to3-migration: {}
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
  # can be removed once this is resolved: https://pulp.plan.io/issues/8701
  pre_tasks:
    - name: install EPEL
      yum:
        name: epel-release
      become: yes
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


Storage
-------

By default, Pulp uses the local filesystem for storage. If you want to use another storage backend such as Amazon Simple Storage Service (S3) or Azure, you’ll need to configure Pulp. To add an Amazon S3 or Azure backend for Pulp using the installer, in your playbook, you must set the necessary variables for your cloud storage in the `pulp_settings` variable of the `pulp_common` role.

1. Create and configure your Amazon S3 or Azure account and gather the credentials that you need to configure the storage backend with Pulp. Follow the instructions in [our Pulpcore storage docs](https://docs.pulpproject.org/pulpcore/installation/storage.html).
2. View the [example playbooks](https://github.com/pulp/pulp_installer/tree/master/playbooks) and note the `pulp_settings` variables for your chosen storage type. Add an entry for each of the variables for your deployment.
3. Use the following examples to populate your own variables in your playbook:

Azure example:
```yaml
pulp_settings:
  secret_key: secret
  content_origin: "{{ pulp_webserver_disable_https | default(false) | ternary('http', 'https') }}://{{ ansible_fqdn }}"
  azure_account_name: 'Storage account name'
  azure_container: 'Container name (as created within the blob service of your storage account)'
  azure_account_key: 'Key1 or Key2 from the access keys of your storage account'
  azure_url_expiration_secs: 60
  azure_overwrite_files: 'True'
  azure_location: 'the folder within the container where your pulp objects will be stored'
  default_file_storage: 'storages.backends.azure_storage.AzureStorage'
```

Amazon S3 example:
```yaml
pulp_settings:
  secret_key: secret
  content_origin: "{{ pulp_webserver_disable_https | default(false) | ternary('http', 'https') }}://{{ ansible_fqdn }}"
  aws_access_key_id: 'AWS Access Key ID'
  aws_secret_access_key: 'AWS Secret Access Key'
  aws_storage_bucket_name: 'pulp3'
  aws_default_acl: "@none None"
  s3_use_sigv4: True
  aws_s3_signature_version: "s3v4"
  aws_s3_addressing_style: "path"
  aws_s3_region_name: "eu-central-1"
  default_file_storage: 'storages.backends.s3boto3.S3Boto3Storage'
  media_root: ''
```

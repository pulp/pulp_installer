Let's Encrypt
=============

Overview
--------

The Pulp 3 Ansible Installer supports obtaining TLS/SSL Certificates via Let's Encrypt (or other
ACME compatible CAs), using your choice of 3rd-party Ansible role.

The pulp_webserver role supports HTTP-01 verification for Let's Encrypt (the most common
verification method), but must be called in a particular manner, as shown in the example playbook
below.

DNS-01 verification is also supported, and guidance is offered below.

Let's Encrypt HTTP-01 Requirements
----------------------------------

Let's Encrypt HTTP-01 verification requires that:

1. The server be accessible over the internet on both ports 80, and 443
  (and 443 per pulp_installer's design.) The Pulp 3 Ansible Installer will configure the OS's firewall, but any
  firewall/router in front of it (such as a security group on a cloud provider) must allow them.

2. The server has a DNS name it can be reached at, such as pulp.example.com . This is what must be
   filled in at `<< domain name >>` in the example playbook below.  Note that many
   auto-generated DNS names by cloud providers are blocked per Let's Encrypt policy.

These requirements must be satisfied before running The Pulp 3 Ansible Installer.

Let's Encrypt HTTP-01 Example Playbook
--------------------------------------
As an example, we are going to write a playbook for installing `pulp_file`, with Let's Encrypt and
HTTP 01 verification.

The 3rd-party role listed below,
[lexa-uw.letsencrypt](https://galaxy.ansible.com/lexa-uw/letsencrypt), is an example. The variables listed below are meant for it, and can serve as a guide for other roles.

You can learn more about the variables on the [roles section](https://pulp-installer.readthedocs.io/en/latest/roles/pulp/#role-variables)

1 -  Install the `pulp_installer` collection:
```
ansible-galaxy collection install pulp.pulp_installer
```

2 -  Install the `geerlingguy.postgresql` role:
```
ansible-galaxy install geerlingguy.postgresql
```

3 - Install your preferred 3rd-party role from [Ansible
Galaxy](https://galaxy.ansible.com/search?deprecated=false&keywords=acme&order_by=-relevance&page=1).

For the example of the role in the playbook below:
```
ansible-galaxy install lexa-uw.letsencrypt
```

4 - Write the following playbook:
```
vim install.yml
```

```yaml
---
- hosts: << domain name >>
  vars:
    pulp_webserver_httpd_servername: "{{ inventory_hostname }}"
    lets_encrypt_hostname: "{{ inventory_hostname }}"
    lets_encrypt_directories_certs: "/etc/letsencrypt"
    lets_encrypt_directories_data: "/var/lib/pulp/pulpcore_static"
    pulp_default_admin_password: << YOUR PASSWORD HERE >>
    pulp_install_plugins:
      # galaxy-ng: {}
      # pulp-ansible: {}
      # pulp-certguard: {}
      # pulp-container: {}
      # pulp-cookbook: {}
      # pulp-deb: {}
      pulp-file: {}
      # pulp-gem: {}
      # pulp-maven: {}
      # pulp-npm: {}
      # pulp-python: {}
      # pulp-rpm: {}
    pulp_settings:
      secret_key: << YOUR SECRET HERE >>
      content_origin: "https://{{ inventory_hostname }}"
  roles:
    # Includes running pulp_webserver. letsencrypt depends on a webserver
    # that can host the .well-known directory.
    - pulp.pulp_installer.pulp_all_services
    - role: lexa-uw.letsencrypt
      become: true
  tasks:
    # Must be run via a task so that it can be run more than once.
    - name: Run pulp_webserver a 2nd time to import the key
      include_role:
        name: pulp.pulp_installer.pulp_webserver
      vars:
        pulp_webserver_tls_key: "/etc/letsencrypt/private_key.pem"
        pulp_webserver_tls_cert: "/etc/letsencrypt/fullchain.pem"
        pulp_webserver_tls_files_remote: true
  environment:
    DJANGO_SETTINGS_MODULE: pulpcore.app.settings
```
4 - Run the playbook:

```
ansible-playbook install.yml -u <managed_node_username> --ask-become-pass
```
<script id="asciicast-335829" src="https://asciinema.org/a/335829.js" async data-autoplay="true" data-speed="2"></script>

Let's Encrypt DNS-01 Verification
---------------------------------
This is supported as well.

The main differences from the above example are:
1. The dropping of the internet accessible requirement, and DNS requirements instead.
2. The 3rd party role for Let's Encrypt is run before `pulp_all_services`/`pulp_webserver`, and
needs a different set of variables.
3. pulp_webserver does not need to be run a 2nd time.
4. When `pulp_all_services`/`pulp_webserver` is run the 1st & only time, specify the
  pulp_webserver_tls variables that point to the certificate and key received in the global `vars`
  section at the top of the playbook.

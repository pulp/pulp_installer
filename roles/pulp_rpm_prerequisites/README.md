Pulp 3 RPM plugin prerequisites
===============================

This role installs prerequisites for pulp-rpm plugin use, when installed by
pulp_installer.

Requirements
------------

Each currently supported operating system has a matching file in the "vars"
directory.

Example Playbook
----------------

Here's an example playbook for using pulp_rpm_prerequisites as part of pulp_installer.

    ---
    - hosts: all
      vars:
        pulp_default_admin_password: password
        pulp_settings:
          secret_key: secret
        pulp_install_plugins:
          pulp-rpm: {}
      roles:
        - pulp_database
        - pulp_workers
        - pulp_resource_manager
        - pulp_webserver
        - pulp_content
      environment:
        DJANGO_SETTINGS_MODULE: pulpcore.app.settings

License
-------

GPLv2+

Author Information
------------------

Pulp Team

# galaxy_post_install

This roles provides post-install configuration for the galaxy-ng plugin.

It runs by default when `galaxy-ng` is part of `pulp_install_plugins` variable. It is called by the
`pulp_common` role.

## Role Variables

* `galaxy_importer_settings`: Key-value dictionary that contains the content of galaxy-importer.cfg to be overwritten.
* `galaxy_create_default_collection_signing_service` Boolean on whether or not to create collection
  signing service. See [Variables for the Collection Signing Service](#variables-for-the-collection-signing-service)
  for additional variables that must be set. Defaults to `false`
* `galaxy_create_default_container_signing_service` Boolean on whether or not to create container
  signing service. See [Variables for the Container Signing Service](#variables-for-the-container-signing-service)
  for additional variables that must be set. Defaults to `false`

## Shared Variables

This role **is tightly coupled** with the required the `pulp_common` role and uses some of
variables which are documented in that role:

* `pulp_certs_dir`: The collection signing service gpg key file is placed under this directory.
* `pulp_scripts_dir`: The collection signing service script is placed under this directory.

## Variables for the Collection Signing Service

If `galaxy_create_default_collection_signing_service==true`:

1. `pulp_settings.galaxy_collection_signing_service` must be set to "ansible-default".
  This variable sets the name of the default collection signing service to use. Defaults to nothing.
2. 2 files must either be specified by these variables:

    * `galaxy_collection_signing_service_key`:  Specify a filepath on the ansible management node.
This is the gpg private key that will be imported to performan the gpg signing of the collections.
Defaults to undefined.
    * `galaxy_collection_signing_service_script` Specify a filepath on the ansible management node.
This is the script that performs the gpg signing of the collections. Defaults to undefined.

Or they must exist on disk (on all pulp hosts e.g. API, content & worker) (these are the paths that
the variables install them to):

* `{{ pulp_certs_dir }}/galaxy_signing_service.gpg` (default: `/etc/pulp/certs/galaxy_signing_service.gpg`):
* `{{ pulp_scripts_dir }}/collection_sign.sh` (default: `/var/lib/pulp/scripts/collection_sign.sh`):

## Variables for the Container Signing Service

If `galaxy_create_default_container_signing_service==true`:

1. `pulp_settings.galaxy_container_signing_service` must be set to "container-default".
  This variable sets the name of the default container signing service to use. Defaults to nothing.

2. 2 files must either be specified by these variables:

    * `galaxy_container_signing_service_key`:  Specify a filepath on the ansible management node.
This is the gpg private key that will be imported to performan the gpg signing of the containers..
Defaults to undefined.
    * `galaxy_container_signing_service_script` Specify a filepath on the ansible management node.
This is the script that performs the gpg signing of the containers. Defaults to undefined.

Or they must exist on disk (on all pulp hosts e.g. API, content & worker) (these are the paths that
the variables install them to):

* `{{ pulp_certs_dir }}/container_signing_service.gpg` (default: `/etc/pulp/certs/container_signing_service.gpg`):
* `{{ pulp_scripts_dir }}/container_sign.sh` (default: `/var/lib/pulp/scripts/container_sign.sh`):

## License

GPLv2+

# Galaxy Post Install

This roles runs galaxy post install configuration
It runs by default when `galaxy-ng` is part of `pulp_install_plugins` variable.

## Role Variables

`galaxy_importer_settings`: Key value dictionnary that contains the content of galaxy-importer.cfg to be overwritten.
`galaxy_create_default_collection_signing_service` Boolean on whether or not to create collection
  signing service. See `Variables for the Signing Service`. Defaults to `false`
`pulp_settings.galaxy_collection_signing_service`: The name of the default signing service to use
  if `galaxy_create_default_collection_signing_service==true`. Defaults to `ansible-default`.

## Shared Variables

This role **is tightly coupled** with the required the `pulp_common` role and uses some of
variables which are documented in that role:

* `pulp_certs_dir`: The collection signing service gpg key file is placed under this directory.
* `pulp_scripts_dir`: The collection signing service script is placed under this directory.

## Variables for the Signing Service

If `galaxy_create_default_collection_signing_service==true`, the 2 files must either
be specified by these variables:

* `galaxy_collection_signing_service_key`:  Specify a filepath on the ansible management node.
This is the gpg private key that will be imported to performan the gpg signing of the collections.
Defaults to undefined.
* `galaxy_collection_signing_service_script` Specify a filepath on the ansible management node.
This is the script that performs the gpg signing of the collections. Defaults to undefined.

Or they must exist on disk (on all pulp hosts e.g. API, content & worker) (these are the paths that
the variables install them to):

* `{{ pulp_certs_dir }}/galaxy_signing_service.gpg` (default: `/etc/pulp/certs/galaxy_signing_service.gpg`):
* `{{ pulp_scripts_dir }}/collection_sign.sh` (default: `/var/lib/pulp/scripts/collection_sign.sh`):

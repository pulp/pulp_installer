# Galaxy Post Install

This roles runs galaxy post install configuration
It runs by default when `galaxy-ng` is part of `pulp_install_plugins` variable.

## Role Variables

`galaxy_importer_settings`: Key value dictionnary that contains the content of galaxy-importer.cfg to be overwritten.
`galaxy_create_default_collection_signing_service` Boolean on whether or not to create collection
  signing service. If set to true the script (default path: /var/lib/pulp/collection_sign.sh)
  and the gpg key file (default path: /etc/pulp/certs/galaxy_signing_service.gpg) must exist,
  you must place them there yourself. Defaults to `false`
`pulp_settings.galaxy_collection_signing_service`: The name of the default signing service to use
  if `galaxy_create_default_collection_signing_service==true`. Defaults to `ansible-default`.

## Shared Variables

This role **is tightly coupled** with the required the `pulp_common` role and uses some of
variables which are documented in that role:

* `pulp_certs_dir` The collection signing service gpg key file must exist under this directory with
  the filename `galaxy_signing_service.gpg` when `galaxy_create_default_collection_signing_service==true`.
* `pulp_scripts_dir`: The collection signing service script must exist under this directory
  with the filename `collection_sign.sh` when `galaxy_create_default_collection_signing_service==true`.

## Required files for the signing service

If `galaxy_create_default_collection_signing_service==true`, the following files must exist on disk.
These must exist on all pulp nodes (API, content & worker).

* `{{ pulp_scripts_dir }}/collection_sign.sh` (default: `/var/lib/pulp/scripts/collection_sign.sh`):
  A script that performs the gpg signing of the collections.
* `{{ pulp_certs_dir }}/galaxy_signing_service.gpg` (default: `/etc/pulp/certs/galaxy_signing_service.gpg`):
  A gpg private key that will be imported to performan the gpg signing of the collections.

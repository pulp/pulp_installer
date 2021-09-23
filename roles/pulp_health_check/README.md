pulp_health_check
=================

Verify if Pulp Services are up and listening.
Note: this role is meant to be run on the host that [pulp_api](https://docs.pulpproject.org/pulp_installer/roles/pulp_api/) is run against

Shared Variables
----------------

This role is **not tightly coupled** to the `pulp_common` role, but uses some of the same
variables. When used in the same play, the values are inherited from the role.
When not used together, this role provides identical defaults.

* `pulp_api_bind`: Set the host the reverse proxy should connect to for the API server. Defaults
  to `127.0.0.1:24817`.
* `pulpcore_version`: Specify a minor version of pulpcore (e.g.: 3.15) one would like to install or upgrade to.
   By default the installer will do the right thing by using the minor version of pulpcore it is designed
   for and tested with. This can also be a specific patch release (e.g.: 3.15.2).

Operating Systems Variables
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

pulp_health_check
=================

Verify if Pulp Services are up and listening.
Note: this role is meant to be run on the host that [pulp_api](https://pulp-installer.readthedocs.io/en/latest/roles/pulp_api/) is run against

Shared Variables
----------------

This role is **not tightly coupled** to the `pulp_common` role, but uses some of the same
variables. When used in the same play, the values are inherited from the role.
When not used together, this role provides identical defaults.

* `pulp_api_bind`: Set the host the reverse proxy should connect to for the API server. Defaults
  to `127.0.0.1:24817`.

Operating Systems Variables
---------------------------

Each currently supported operating system has a matching file in the "vars"
directory.

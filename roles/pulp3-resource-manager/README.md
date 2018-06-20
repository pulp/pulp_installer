pulp3-resource-manager
=============

Install, configure, and set the state of the pulp resouce manager.

This role accepts two optional variables:

- `pulp_resouce_manager_state`:
  This variable can be configured with any of the states allowed by the systemd
  module's "state" directive. Optional. Defaults to "started."
- `pulp_resouce_manager_enabled`:
  This variable can be configured with any of the enableds allowed by the
  systemd module's "enabled" directive. Optional. Defaults to "true."

Split the pulp_database role into pulp_database (installs postgres database)
and pulp_database_config (configures Pulp database) for the sake of proper
design. pulp_database no longer depends on pulp_common, so it can now be run
against a separate database server without Pulp installed.

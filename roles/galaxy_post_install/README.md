# Galaxy Post Install

This roles runs galaxy post install configuration
It runs by default when `galaxy-ng` is part of `pulp_install_plugins` variable.

## Tasks

### Galaxy Importer Settings

Creates config file for galaxy-importer

#### Variables

`galaxy_importer_settings`: Key value dictionnary that contains the content of galaxy-importer.cfg to be overwritten.

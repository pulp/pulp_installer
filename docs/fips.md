FIPS
====

When `ansible` detects that the target node to run in a FIPS enviroment, the installer will adjust
some aspects of the installation:

1. If installing from `PyPi`, the installer will fetch a specially patched version of `django`.
  The same version will be provided packaged as rpm.

2. A default for `allowed_content_checksums` will be set that does not include `MD5`. You might
  consider adjusting that value to the site specific recommendations in your playbooks variable
  `pulp_settings`.

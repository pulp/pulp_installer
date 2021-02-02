#!/usr/bin/env bash

# This script moves a directory passed in the first parameter to the location passed in as a second
# parameter. It then creates a symlink from the old location to the new. When SELinux is enabled,
# SELinux contexts are preserved.

# Fail if the mv or ln fail
set -e

mv -Z $1 $2
ln -s $2 $1

# Don't fail if 'getenforce' command is not present
set +e

command -v selinuxenabled

if [ $? == 0  ]; then
  set -e
  if selinuxenabled ; then
    restorecon $1
  fi
fi

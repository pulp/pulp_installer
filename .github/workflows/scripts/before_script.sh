#!/usr/bin/env bash

set -xmveuo pipefail

group=libvirt
# Re-launch the script with libvirt as the primary group.
# Needed because we just created the group and added the GHA runner use to it.
# Avoids running vagrant as root.
if [ $(id -gn) != $group ]; then
  exec sg $group "$0 $*"
fi


BOX=$(echo "$1" | cut -d '-' -f3-)
echo $BOX
vagrant box add pulp/$BOX

#!/usr/bin/env bash

group=libvirt
# Re-launch the script with libvirt as the primary group.
# Needed because we just created the group and added the GHA runner use to it.
# Avoids running vagrant as root.
if [ $(id -gn) != $group ]; then
  exec sg $group "$0 $*"
fi

echo "Need to debug? Please check: https://github.com/marketplace/actions/debugging-with-tmate"
vagrant ssh $1 -c "http --timeout 30 --check-status --pretty format --print hb http://127.0.0.1/pulp/api/v3/status/" || \
vagrant ssh $1 -c "curl http://127.0.0.1:24817/pulp/api/v3/status/" || true
vagrant ssh $1 -c "sudo systemctl status pulpcore-api" || true
vagrant ssh $1 -c "sudo journalctl -u pulpcore-api" || true

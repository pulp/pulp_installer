#!/usr/bin/env bash

set -xmveuo pipefail

sed -i -e 's/memory: 10500/memory: 5500/g' vagrant/boxes.d/*
sed -i -e 's/cpus: 4/cpus: 2/g' vagrant/boxes.d/*

unset GEM_PATH
unset GEM_HOME
# We do this because we could not set newgrp earlier
sudo vagrant up $1

# If these start getting low, add a swapfile. Under / on Travis, or /mnt on GHA.
echo "VM RAM:"
sudo vagrant ssh $1 -c "free -m"
echo "Host RAM:"
free -m

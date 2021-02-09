#!/usr/bin/env bash

set -xmveuo pipefail

group=libvirt
# Re-launch the script with libvirt as the primary group.
# Needed because we just created the group and added the GHA runner use to it.
# Avoids running vagrant as root.
if [ $(id -gn) != $group ]; then
  exec sg $group "$0 $*"
fi

sed -i -e 's/memory: 10500/memory: 5500/g' vagrant/boxes.d/*
sed -i -e 's/cpus: 4/cpus: 2/g' vagrant/boxes.d/*

unset GEM_PATH
unset GEM_HOME

# Workaround limitation of EL7's old postgres 9.6:
# https://pulp.plan.io/issues/7993
sudo localectl set-locale en_US.UTF-8
export LANG=en_US.UTF-8
sudo localectl status
localectl status

# Workaround https://pulp.plan.io/issues/8095 until fixed.
if [[ "$1" == *"fips" ]] ; then
  cp .github/files/fips/requirements.yml ./requirements.yml
fi

# This comamnd does include vagrant-sshfs getting run, and thus using epel.
# --no-tty --machine-readable and the grep is an overall approach to avoid clutter
# in the output during box download, it would do a progress bar.
set -o pipefail
if vagrant up --no-tty --machine-readable --no-destroy-on-error --no-provision $1 | grep -v -e '^\s*$' ; then
  /bin/true
else
  # Workaround inability to contact EPEL7, triggered by vagrant-sshfs
  # trying to install fuse-sshfs.
  # Seems only to occur on GHA, probably due to a transparent proxy or
  # something similar in their network.
  #
  # The error manifests as:
  # default epel.repo config, with a metalink:
  # Cannot retrieve metalink for repository: epel/x86_64. Please verify its path and try again
  # epel.repo configured to use a baseurl of osuosl:
  # [Errno 14] HTTPS Error 302 - Found
  # curl: (77) Problem with the SSL CA cert (path? access rights?)
  #
  # The curl error is seems misleading though, the files seem to be accessible,
  # particularly when curl is run as root. They might be corrupted, but I can
  # regenerate them.
  # vagrant ssh $1 -- "sudo sed -i '/\[epel\]/a sslverify=0' /etc/yum.repos.d/epel.repo"
  # vagrant sshfs --mount $1

  # Workaround a bug in libvirt 6.6.0 (20.04 + virtualization ppa) on non-btrfs.
  sudo virsh pool-start default
  vagrant up --no-tty --machine-readable --no-destroy-on-error --no-provision $1 | grep -v -e '^\s*$'
fi
set +o pipefail

echo 'QEMU COMMAND RUNNING. Look for "tcg" as the acceleration method:'
ps -ef | grep qemu

vagrant provision $1

# If these start getting low, add a swapfile. Under / on Travis, or /mnt on GHA.
echo "VM RAM:"
vagrant ssh $1 -c "free -m"
echo "Host RAM:"
free -m

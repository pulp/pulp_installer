#!/usr/bin/env bash

set -xmveuo pipefail

sudo apt update

sudo apt install software-properties-common

# Virtualization stack upgrades, has Qemu 5.0
sudo add-apt-repository ppa:jacob/virtualisation

# Provides Qemu 5.2. It is needed because on Qemu 4.2 / 5.0 , CentOS 7 guests have a number
# of weird errors, including Postgres database creation and SSL certificate
# validation in curl and yum.
sudo add-apt-repository ppa:pulpproject/pulp-ci

# Provides a newer "vagrant" package that is compatible with Ubuntu 20.04
sudo add-apt-repository ppa:tiagohillebrandt/vagrant

if /bin/false ; then
  # 2.2.9 is needed for proper CentOS8 support
  VAGRANT_DEB=vagrant_2.2.19+dfsg-1ubuntu1_all.deb
  curl -L --output $VAGRANT_DEB http://mirrors.kernel.org/ubuntu/pool/universe/v/vagrant/$VAGRANT_DEB
  sudo apt install ./$VAGRANT_DEB
  rm ./$VAGRANT_DEB
fi

# Updating vagrant & vagrant-sshfs is necessary to support CentOS 7,8,8-stream without repos pre-configured.
VAGRANT_SSHFS_DEB=vagrant-sshfs_1.3.6-1_all.deb
curl -L --output $VAGRANT_SSHFS_DEB http://mirrors.kernel.org/ubuntu/pool/universe/v/vagrant-sshfs/$VAGRANT_SSHFS_DEB
sudo apt install ./$VAGRANT_SSHFS_DEB
rm ./$VAGRANT_SSHFS_DEB

# Updating ansible past 2.9.6 (to 2.9.8+) is necessary to manage Fedora 32:
# https://github.com/ansible/ansible/pull/68211
# And to 2.9.16 for a bug with managing systemd
# https://github.com/ansible/ansible/issues/71528#issuecomment-729778048
sudo apt remove ansible
pip3 install -U pip
pip3 install "ansible>2.9.15"

# qemu-kvm has gone from a tiny package to a virtual package in Qemu 5.2.
# Workaround the PPA's virtual package not existing or properly depending on qemu-system-x86.
sudo apt install qemu-kvm || sudo apt install qemu-system-x86

sudo apt install openssh-server vagrant-libvirt libvirt-daemon-system qemu-utils cpu-checker dnsmasq

# We may need to use upstream Vagrant version in the future, but for now the
# new debs are faster.
if /bin/false ; then
  VAGRANT_DEB=vagrant_2.2.14_x86_64.deb
  curl -O https://releases.hashicorp.com/vagrant/2.2.14/$VAGRANT_DEB
  sudo apt install ./$VAGRANT_DEB
  rm ./$VAGRANT_DEB

  # Steps for vagrant-libvirt
  sudo sed -i "s/# deb-src/deb-src/g" /etc/apt/sources.list
  sudo apt update
  sudo apt build-dep vagrant ruby-libvirt
  sudo apt install qemu libvirt-daemon-system libvirt-clients ebtables dnsmasq-base
  sudo apt install libxslt-dev libxml2-dev libvirt-dev zlib1g-dev ruby-dev

  vagrant plugin install vagrant-libvirt
  sudo vagrant plugin install vagrant-libvirt

  vagrant plugin install vagrant-sshfs
  sudo vagrant plugin install vagrant-sshfs
fi

# Increase timeout for CI jobs
sed -i "s/pulp_service_timeout: 90/pulp_service_timeout: 180/g" roles/pulp_common/defaults/main.yml

# Use unix socket
sed -e "/pulp_default_admin_password/a pulp_content_bind: 'unix:/var/run/pulpcore-content/pulpcore-content.sock'" example.dev-config.yml > local.dev-config.yml
sed -i "/pulp_default_admin_password/a pulp_api_bind: 'unix:/var/run/pulpcore-api/pulpcore-api.sock'" local.dev-config.yml
cat local.dev-config.yml

if sudo kvm-ok ; then
  # Speed up disk writes by switching qemu-kvm from writeback to unsafe.
  ln -s $PWD/vagrant/settings.ci.yaml forklift/vagrant/settings.yaml
else
  # GHA: Fallback to Qemu emulation so long as GHA does not support nested virt
  cp -p $PWD/.github/files/qemu/settings.yaml forklift/vagrant/settings.yaml
fi
sudo usermod -a -G libvirt $USER
sudo systemctl enable --now ssh
sudo systemctl enable --now libvirtd

echo "VAGRANT PLUGINS AS USER:"
vagrant plugin list
echo "VAGRANT PLUGINS AS SUDO:"
sudo vagrant plugin list

free -m
df -h
df -hl
cat /proc/cpuinfo
sudo apt install virt-what
sudo virt-what

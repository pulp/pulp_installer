#!/usr/bin/env bash

set -xmveuo pipefail

sudo apt update

# Updating vagrant-sshfs is necessary to support CentOS 7,8 without repos pre-configured.
curl -L --output vagrant-sshfs_1.3.4-1_all.deb http://ftp.br.debian.org/debian/pool/main/v/vagrant-sshfs/vagrant-sshfs_1.3.4-1_all.deb
sudo apt install ./vagrant-sshfs_1.3.4-1_all.deb
rm ./vagrant-sshfs_1.3.4-1_all.deb

sudo apt install software-properties-common openssh-server vagrant-libvirt libvirt-daemon-system vagrant-sshfs qemu-utils qemu-kvm cpu-checker dnsmasq
# This PPA doesn't exist for 20.04 (focal)
if grep -i bionic /etc/os-release ; then
  sudo apt-add-repository --yes --update ppa:ansible/ansible
fi

# Updating ansible past 2.9.6 (to 2.9.8+) is necessary to manage Fedora 32:
# https://github.com/ansible/ansible/pull/68211
if grep -i focal /etc/os-release ; then
  # The 20.10 (groovy) version. Still Python 3.8
  curl -L --output ansible_2.9.9+dfsg-1_all.deb http://mirrors.kernel.org/ubuntu/pool/universe/a/ansible/ansible_2.9.9+dfsg-1_all.deb
  sudo apt install ./ansible_2.9.9+dfsg-1_all.deb
  sudo rm ./ansible_2.9.9+dfsg-1_all.deb
fi

sudo apt install ansible
sudo kvm-ok
sudo usermod -a -G libvirt $USER
sudo systemctl enable --now ssh
sudo systemctl enable --now libvirtd
# newgrp - libvirt # This causes Travis to hang, with or without the dash

# Speed up disk writes by switching qemu-kvm from writeback to unsafe.
ln -s $PWD/vagrant/settings.ci.yaml forklift/vagrant/settings.yaml

free -m
df -h
df -hl
cat /proc/cpuinfo
sudo apt install virt-what
sudo virt-what

# For the source tests
cd ..
git clone https://github.com/pulp/pulpcore
git clone https://github.com/pulp/pulp_file

#!/bin/bash

BASEDIR=$(dirname "$0")

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo"
  exit
fi

if [ "$1" == "prepare" ]; then
  # Install aptitude which is necessary for Ansible
  apt install aptitude

  # Install the latest version of Ansible from the PPA repository
  apt-add-repository ppa:ansible/ansible
  apt update
  apt install ansible -y

  # Create SSH key pair for the root user
  ssh-keygen -f /root/.ssh/id_rsa -N ""
  cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

  # Create SSH key pair for the sysadm user
  mkdir -p /home/sysadm/.ssh
  ssh-keygen -f /home/sysadm/.ssh/id_rsa -N ""
  chown -R sysadm:sysadm /home/sysadm/.ssh

  # Create the LVM
  ansible-playbook -i $BASEDIR/../python/get-ansible-inventory.py $BASEDIR/../ansible/host-prepare.yaml

else
  echo "Prepares the host machine for the platform installation"
  echo "Usage:"
  echo "  host.sh prepare"
fi

#!/bin/bash

BASEDIR=$(dirname "$0")
ACTION=$1

RED=`tput setaf 1`
GREEN=`tput setaf 2`
NC=`tput sgr0`

# Install Linux packages which are necessary to determine configuration parameters
apt install python3-pip -y && pip3 install pyyaml

function write_title() {
  echo
  printf "     *"; for ((i=0; i<${#1}; i++)); do printf "*"; done; printf "*"; echo
  printf "***** $1 "; for ((i=0; i<`tput cols` - ${#1} - 7; i++));do printf "*"; done; echo
  echo
}

if [ "$EUID" -ne 0 ]
  then echo "Please run as root or with sudo"
  exit
fi

if [ "$ACTION" == "prepare" ]; then
   # Install aptitude which is necessary for Ansible
  apt install aptitude python3-pip -y

  # Install Python packages
  pip install pyyaml

  # Install Ansible
  apt install ansible apache2-utils -y

elif [ "$ACTION" == "install" ]; then
  # Add the nodes to the hosts file of each virtual machine
  write_title "Executing ansible/hosts.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/hosts.yaml

  # Install Docker on each virtual machine
  write_title "Executing ansible/docker.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/docker.yaml

  # Prepare all Kubernetes nodes with a basic installation
  write_title "Executing ansible/kubernetes-prepare.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-prepare.yaml

  # Install the Kubernetes management
  write_title "Executing ansible/kubernetes-management.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-management.yaml

  # Install the worker nodes
  write_title "Executing ansible/kubernetes-nodes.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-nodes.yaml

  # Install the base components
  write_title "Executing ansible/kubernetes-base.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-base.yaml

  # Install the storage components
  write_title "Executing ansible/kubernetes-storage.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-storage.yaml

  # Install the monitoring solution
  write_title "Executing ansible/kubernetes-monitoring.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-monitoring.yaml

  # Install the Ingress implementation
  write_title "Executing ansible/kubernetes-ingress.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-ingress.yaml

  # Create port forwarding rules into the Kubernetes cluster
  write_title "Executing ansible/kubernetes-firewall.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-firewall.yaml

  # Install the Docker Registry
  write_title "Executing ansible/kubernetes-dockerreg.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-dockerreg.yaml

  # Deploy custom namespaces
  write_title "Executing ansible/kubernetes-customns.yaml"
  ansible-playbook -i $BASEDIR/python/get-ansible-inventory.py $BASEDIR/ansible/kubernetes-customns.yaml

else
  echo "Deploys a Kubernetes cluster"
  echo "Usage:"
  echo "  platform.sh prepare"
  echo "  platform.sh install"

fi

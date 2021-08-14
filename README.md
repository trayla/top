# TOP - Trayla Operations Platform

Note: The master branch may be in an unstable or even broken state during development. Please use releases instead of the master branch in order to get a stable set of binaries.

## Prerequisits

### Hardware requirements

- At least one running machine with a plain Ubuntu 20.04 Server installation and root access. Virtual machines are supported as well as bare metal installations.
- Minimum 8 GB RAM on each node
- Minimum 100 GB storage

### Knowledge

- An understanding of Linux based system management and command line tools
- Knowledge about operating a Kubernetes platform

#### Install scripts

In order to execute the scripts you have to clone this GitHub repository to your server into the directory /opt/mgmt/top by issuing the following commands:
```ShellSession
mkdir -p /opt/mgmt/top
git clone https://github.com/trayla/top.git /opt/mgmt/top
```

The values file defines specific customizations of your own topology. A sample file is included in this repository. It should be copied to /opt/mgmt and customized before further installation.
```ShellSession
cp /opt/mgmt/top/values-default.yaml /opt/mgmt/values-top.yaml
```

#### Domain

The Trayla Operations Platform provides a some to the outside world. In order to access these services we are registering them as sub domains of a configurable main domain. The most comfortable way is to have a main domain like 'example.com' which points to your platform IP address by a wildcard DNS entry like this '*.example.com > 88.77.66.55'. In this case the platform can route any subdomain to the desired service by itself.

## Usage

Prepare your host with the following command. This is necessary only once while you can install and remove the platform from your host as much as you like.
```ShellSession
sudo /opt/mgmt/top/platform.sh prepare
```

Install the platform with the following command.
```ShellSession
sudo /opt/mgmt/top/platform.sh install
```

After completion the system will be restarted. It takes a couple minutes until all virtual machines and services are up an running.

## Result

If everything worked as expected you should have the following setting on your machine.

### Architectural Overview

This picture shows an architectural overview of the desired platform:

![Diagram](docs/landscape.svg)

<a href="https://app.diagrams.net/#Htrayla%2Fssp%2Fmaster%2Fdocs%2Flandscape.svg" target="_blank">Edit</a>

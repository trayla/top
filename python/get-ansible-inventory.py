#!/usr/bin/python3

import os
import sys
import argparse
import yaml
import simplejson

platform_domain = ''
platform_name = ''
platform_console = ''
platform_nodes = ''
platform_nodes_controlplanes = ''
platform_nodes_workers = ''
with open("/opt/mgmt/values-top.yaml", 'r') as stream:
  try:
    platform = yaml.safe_load(stream).get("platform")
    platform_domain = platform.get("domain")
    platform_name = platform.get("name")
    platform_console = platform.get("console")
    platform_nodes = platform.get("nodes")
    platform_nodes_controlplanes = platform_nodes.get("controlplanes")
    platform_nodes_workers = platform_nodes.get("workers")
  except yaml.YAMLError as exc:
    platform_console = ''

class Inventory(object):

  def __init__(self):
    self.inventory = {}
    self.read_cli_args()

    # Called with `--list`.
    if self.args.list:
      self.inventory = self.get_inventory()
    # Called with `--host [hostname]`.
    elif self.args.host:
      # Not implemented, since we return _meta info `--list`.
      self.inventory = self.empty_inventory()
    # If no groups or vars are present, return an empty inventory.
    else:
      self.inventory = self.empty_inventory()

    print(simplejson.dumps(self.inventory))

  # Example inventory for testing
  def get_inventory(self):
    controlplanes = []
    workers = []
    jsHostvars = {}

    jsHostvars['console'] = {
      'ansible_host': platform_console.get("ip"),
      'ansible_fqcn': "console." + platform_name + "." + platform_domain,
      'ansible_user': 'root',
      'ansible_ssh_common_args': '-o StrictHostKeyChecking=no'
    }

    count = 1
    for nodeName in platform_nodes_controlplanes.keys():
      jsHostvars[nodeName] = {
        'ansible_host': platform_nodes_controlplanes[nodeName].get("ip"),
        'ansible_fqcn': nodeName + "." + platform_name + "." + platform_domain,
        'ansible_user': 'root',
        'ansible_ssh_common_args': '-o StrictHostKeyChecking=no'
      }
      controlplanes.append(nodeName)
      count = count + 1

    count = 1
    if platform_nodes_workers != None:
      for nodeName in platform_nodes_workers.keys():
        jsHostvars[nodeName] = {
          'ansible_host': platform_nodes_workers[nodeName].get("ip"),
          'ansible_fqcn': nodeName + "." + platform_name + "." + platform_domain,
          'ansible_user': 'root',
          'ansible_ssh_common_args': '-o StrictHostKeyChecking=no'
        }
        workers.append(nodeName)
        count = count + 1

    return {
      'all': {
        'hosts': [ 'console' ],
        'children': [ 'kubernetes' ]
      },
      'kubernetes': {
        'hosts': controlplanes,
        'children': [ 'workers' ]
      },
      'workers': {
        'hosts': workers
      },
      '_meta': {
        'hostvars': jsHostvars
      }
    }

  # Empty inventory for testing
  def empty_inventory(self):
    return {'_meta': {'hostvars': {}}}

  # Read the command line args passed to the script
  def read_cli_args(self):
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action = 'store_true')
    parser.add_argument('--host', action = 'store')
    self.args = parser.parse_args()

# Get the inventory
Inventory()

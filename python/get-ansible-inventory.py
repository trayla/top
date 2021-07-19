#!/usr/bin/python3

import os
import sys
import argparse
import yaml
import simplejson

platform_nodes_console = ''
with open("/opt/mgmt/values-top.yaml", 'r') as stream:
  try:
    platform_nodes_console = yaml.safe_load(stream).get("platform").get("nodes").get("console").get("ip")
  except yaml.YAMLError as exc:
    platform_nodes_console = ''

platform_nodes_master1 = ''
with open("/opt/mgmt/values-top.yaml", 'r') as stream:
  try:
    platform_nodes_master1 = yaml.safe_load(stream).get("platform").get("nodes").get("master1").get("ip")
  except yaml.YAMLError as exc:
    platform_nodes_master1 = ''

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
    return {
      'all': {
        'hosts': [ 'console' ],
        'children': [ 'kubernetes' ]
      },
      'kubernetes': {
        'hosts': [ 'master1' ],
        'children': [ 'workers' ]
      },
      'workers': {
        'hosts': [ ]
      },
      '_meta': {
        'hostvars': {
          'console': {
            'ansible_host': platform_nodes_console,
            'ansible_user': 'root',
            'ansible_ssh_common_args': '-o StrictHostKeyChecking=no'
          },
          'master1': {
            'ansible_host': platform_nodes_master1,
            'ansible_user': 'root',
            'ansible_ssh_common_args': '-o StrictHostKeyChecking=no'
          }
        }
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

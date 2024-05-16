import sys
import pathlib
import time
import signal
import glob
import subprocess

import config_files.sut_config as sut_config
import config_files.slicify_config as slicify_config

def inject_partial_partition(node_ip_1, node_ip_2):
  """
    Run iptables command to break connection between nodes, creating a partial partition between them.
    Note that other nodes can still access both of these nodes
  """
  subprocess.run(['ssh', node_ip_1, '&&', 'sudo', 'iptables', '-A', 'INPUT', '-s', node_ip_2, '-j', 'DROP'])
  subprocess.run(['ssh', node_ip_2, '&&', 'sudo', 'iptables', '-A', 'INPUT', '-s', node_ip_1, '-j', 'DROP'])


def inject_complete_partition(node_ip):
  """
    Use iptables to block connections to all other nodes from target node, creating a complete partition
  """

  for cluster_node in slicify_config.cluster_nodes:
    if(cluster_node != node_ip):
      subprocess.run(['ssh', node_ip, '&&', 'sudo', 'iptables', '-A', 'INPUT', '-s', cluster_node, '-j', 'DROP'])

def heal_partial_partition(node_ip_1, node_ip_2):
  """
    Heals partial partition by removing iptables rules from both nodes
  """

  subprocess.run(['ssh', node_ip_1, '&&', 'sudo', 'iptables', '-D', 'INPUT', '-s', node_ip_2, '-j', 'DROP'])
  subprocess.run(['ssh', node_ip_2, '&&', 'sudo', 'iptables', '-D', 'INPUT', '-s', node_ip_1, '-j', 'DROP'])

def heal_complete_partition(node_ip):
  """
    Heal complete partition by removing iptables rules from target node
  """
  for cluster_node in slicify_config.cluster_nodes:
    if(cluster_node != node_ip):
      subprocess.run(['ssh', node_ip, '&&', 'sudo', 'iptables', '-D', 'INPUT', '-s', cluster_node, '-j', 'DROP'])

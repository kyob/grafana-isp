#!/usr/bin/env python

import config
import sys
import time
import select
import paramiko
import re
import requests

from influxdb import InfluxDBClient

def connect_to_host(host):
    i = 1
    while True:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host,port=config.ssh_port,username=config.ssh_user,password=config.ssh_password)
            break
        except paramiko.AuthenticationException:
            sys.exit(1)
        except:
            i += 1
            time.sleep(2)
            if i == 30:
                sys.exit(1)

    stdin, stdout, stderr = ssh.exec_command(config.nexus_command_macs)
    output = stdout.readlines()
    macs = re.search("\d+", str(output))
    macs = int(macs.group())

    stdin, stdout, stderr = ssh.exec_command(config.nexus_command_multicast_macs)
    output = stdout.readlines()
    macs_multicast = re.search("\d+", str(output))
    macs_multicast = int(macs_multicast.group())

    stdin, stdout, stderr = ssh.exec_command(config.nexus_command_control_plane_arp_drop)
    output = stdout.readlines()
    arp_drop = re.search("\d+", str(output))
    arp_drop = int(arp_drop.group())

    stdin, stdout, stderr = ssh.exec_command(config.nexus_command_control_plane_arp_out)
    output = stdout.readlines()
    arp_out = re.search("\d+", str(output))
    arp_out = int(arp_out.group())

    stdin, stdout, stderr = ssh.exec_command(config.nexus_command_control_plane_arp_police)
    output = stdout.readlines()
    arp_police_pps = re.search("\d+", str(output))
    arp_police_pps = int(arp_police_pps.group())

    data = [
    {
    "measurement":"macs",
    "tags":{
        "host":host
        },
     "fields":{
      "value":macs
      }
      },
    {
    "measurement":"macs_multicast",
    "tags":{
        "host":host
        },
     "fields":{
      "value":macs_multicast
      }
      },
    {
    "measurement":"arp_drop",
    "tags":{
        "host":host
        },
     "fields":{
      "value": arp_drop
      }
      },
    {
    "measurement":"arp_out",
    "tags":{
        "host":host
        },
     "fields":{
      "value": arp_out
      }
      },
    {
    "measurement":"arp_police_pps",
    "tags":{
        "host":host
        },
     "fields":{
      "value": arp_police_pps
      }
      }
    ]

    if config.debug == 1:
	print(data)
    else:
       dbClient = InfluxDBClient(host=config.influxdb_host, port=config.influxdb_port, database=config.influxdb_db)
       dbClient.write_points(data)

    ssh.close()

for host in config.hosts:
    connect_to_host(host)


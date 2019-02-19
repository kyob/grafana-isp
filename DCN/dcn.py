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
            ssh.connect(host,port=config.ssh_port,username=config.ssh_username,password=config.ssh_password)
            break
        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s" % host
            sys.exit(1)
        except:
            print "Could not SSH to %s, waiting for it to start" % host
            i += 1
            time.sleep(2)
            if i == 3:
                print "Could not connect to %s. Giving up" % host
                sys.exit(1)

    # Send the command (non-blocking)
    stdin, stdout, stderr = ssh.exec_command(config.ssh_command)
    output = stdout.readlines()
    for i in range(len(output)):
        if i==9:
            macs = re.search("\d+", str(output[i]))
            macs = int(macs.group())

    influxdb_data = [
    {
    "measurement":"macs",
    "tags":{
        "host":host
        },
     "fields":{
      "value":macs
      }
      }
    ]
    print(influxdb_data)
    #dbClient = InfluxDBClient(host=config.influxdb_host, port=config.influxdb_port, database=config_influxdb_db)
    #dbClient.write_points(influxdb_data)
    ssh.close()

for host in config.hosts:
    connect_to_host(host)


#!/usr/bin/env python

import config
import paramiko
import time
import json
import sys
import select
import re
import requests

from influxdb import InfluxDBClient


def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output


def connect_to_host(host_ip):

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
         paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(host_ip, username=config.ssh_user, password=config.ssh_password)
    #print "--- SSH connection established to %s ---" % options.ip

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    #print "--- Interactive SSH session established ---"

    # Strip the initial router prompt
    output = remote_conn.recv(1000)

    # See what we have
    #print output

    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n")

    # Get output in json format
    remote_conn.send(config.nexus_command_enviroment_power_input)

    # Wait for the command to complete
    time.sleep(2)

    output = remote_conn.recv(50000)

    #print 'output', output

    # Get second line which is the json output
    output = output.split("\n")[2]

    j = json.loads(output)

    powersup = j['powersup']['TABLE_psinputinfo_n3k']['ROW_psinputinfo_n3k']
    ps_slot_1 = int(powersup['ps_slot'][0])
    ps_input_voltage_1 = float(powersup['ps_input_voltage'][0])
    ps_input_current_1 = float(powersup['ps_input_current'][0])
    ps_in_power_1 = float(powersup['ps_in_power'][0])
    ps_state_1 = powersup['ps_state'][0]
    if ps_state_1 == 'ok':
        ps_state_1 = 1
    else:
        ps_state_1 =  0

    ps_slot_2 = int(powersup['ps_slot'][1])
    ps_input_voltage_2 = float(powersup['ps_input_voltage'][1])
    ps_input_current_2 = float(powersup['ps_input_current'][1])
    ps_in_power_2 = float(powersup['ps_in_power'][1])
    ps_state_2 = powersup['ps_state'][1]
    if ps_state_2 == 'ok':
        ps_state_2 = 1
    else:
        ps_state_2 =  0

    data1 = [
    {
    "measurement":"ps_slot_1",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value":ps_slot_1
      }
      },
    {
    "measurement":"ps_input_voltage_1",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value":ps_input_voltage_1
      }
      },
    {
    "measurement":"ps_input_current_1",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value": ps_input_current_1
      }
      },
    {
    "measurement":"ps_in_power_1",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value": ps_in_power_1
      }
      },
    {
    "measurement":"ps_state_1",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value": ps_state_1
      }
      }
    ]


    data2 = [
    {
    "measurement":"ps_slot_2",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value":ps_slot_2
      }
      },
    {
    "measurement":"ps_input_voltage_2",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value":ps_input_voltage_2
      }
      },
    {
    "measurement":"ps_input_current_2",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value": ps_input_current_2
      }
      },
    {
    "measurement":"ps_in_power_2",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value": ps_in_power_2
      }
      },
    {
    "measurement":"ps_state_2",
    "tags":{
	"host":host_ip
        },
     "fields":{
      "value": ps_state_2
      }
      }
    ]


    if config.debug == 1:
	print(data1)
	print(data2)
    else:
        dbClient = InfluxDBClient(host=config.influxdb_host, port=config.influxdb_port, database=config.influxdb_db)
        dbClient.write_points(data1)
        dbClient.write_points(data2)

    remote_conn.close()

for host_ip in config.hosts:
    connect_to_host(host_ip)


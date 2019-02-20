#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import mysql.connector
from influxdb import InfluxDBClient

mydb = mysql.connector.connect(
  host = config.mysql_host,
  user = config.mysql_user,
  passwd = config.mysql_password,
  database = config.mysql_database
)

mycursor = mydb.cursor()
mycursor.execute(config.mysql_query_klienci)
myresult = mycursor.fetchall()

dbClient = InfluxDBClient(host = config.influxdb_host, port = config.influxdb_port, database = config.influxdb_db_klienci)

for x in myresult:
    data = [
    {
        "measurement":"klienci",
        "tags": {
            "name":"aktywni"
        },
        "fields": {
            "value":x[0]
        }
    },
    {
        "measurement":"klienci",
        "tags": {
            "name":"usunieci"
        },
        "fields": {
            "value":x[1]
        }
    },
    {
        "measurement":"klienci",
        "tags": {
            "name":"wszyscy"
        },
        "fields": {
            "value":x[2]
        }
    },
    ]

    if config.debug_taryfy == 1:
    	print(data)
    else:
	dbClient.write_points(data)



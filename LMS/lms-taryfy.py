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
mycursor.execute(config.mysql_query_taryfy)
myresult = mycursor.fetchall()

dbClient = InfluxDBClient(host = config.influxdb_host, port = config.influxdb_port, database = config.influxdb_db_taryfy)

for x in myresult:
    data = [
    {
        "measurement": "taryfy",
        "tags": {
            "name": x[1]
        },
        "fields": {
            "value": x[0]
        }
    },
    ]
    if config.debug_taryfy == 1:
	print(data)
    else:
	dbClient.write_points(data)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import api

def create_db_cloud(cloudname):
    try:
        conn.execute(f'''CREATE TABLE '{cloudname}'
                (TYPE           TEXT    NOT NULL,
                DATA           TEXT    NOT NULL);''')
    except:
        print (f"Table {cloudname} already exist")

def list_db_table():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

def delete_db_table(table):
    cursor.execute(f"DROP TABLE {table}")

def insert_db_data(cloud_name, prout, data):
    for i in data:
        #sql = f'''INSERT INTO {cloud} (TYPE, DATA) VALUES ({type},{i})'''
        sql = f'''INSERT INTO {cloud_name} (TYPE, DATA) VALUES ("{prout}","{i}")'''
        conn.execute(sql)
        conn.commit()

def readSqliteTable(cloud_name, type):
    try:
        sqlite_select_query = f"""SELECT * from {cloud_name}"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        for row in records:
            if (type == "ALL"):
                print(f"{row[0]} - {row[1]}")
                
            elif (row[0] == type):
                print(row[1])

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)


def fill_database(cloud_name):
    cloud = api.cloud_connection(cloud_name)
    data = api.list_flavors(cloud).values()
    insert_db_data(cloud_name, "FLAVOR", data)
    data = api.list_images(cloud).values()
    insert_db_data(cloud_name, "IMAGE", data)
    data = api.list_networks(cloud).values()
    insert_db_data(cloud_name, "NETWORK", data)
    data = api.list_security_groups(cloud).values()
    insert_db_data(cloud_name, "SECURITY_GROUP", data)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

create_db_cloud("Infomaniak")
list_db_table()
cloud_name = 'Infomaniak'
fill_database(cloud_name)
readSqliteTable(cloud_name, "ALL")
delete_db_table(cloud_name)
conn.close()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
#import openstack_api

def connect_to_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    return conn, cursor

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
    cloud = openstack_api.cloud_connection(cloud_name)
    data = openstack_api.list_flavors(cloud).values()
    insert_db_data(cloud_name, "FLAVOR", data)
    data = openstack_api.list_images(cloud).values()
    insert_db_data(cloud_name, "IMAGE", data)
    data = openstack_api.list_networks(cloud).values()
    insert_db_data(cloud_name, "NETWORK", data)
    data = openstack_api.list_security_groups(cloud).values()
    insert_db_data(cloud_name, "SECURITY_GROUP", data)

def insert_api_key(key):
    conn, cursor = connect_to_db()
    query = f"INSERT IGNORE INTO api_keys (key) VALUES('{key}');"
    cursor.execute(query)
    conn.commit()
    conn.close()

def seek_api_key(key):
    conn, cursor = connect_to_db()
    query = f"SELECT key FROM api_keys WHERE key='{key}';"
    result = cursor.execute(query)
    conn.close
    return result.fetchone()

# create_db_cloud("Infomaniak")
# list_db_table()
# cloud_name = 'Infomaniak'
# fill_database(cloud_name)
# readSqliteTable(cloud_name, "ALL")
# delete_db_table(cloud_name)
# conn, cursor = connect_to_db()
# # #cmd = "CREATE TABLE api_keys(key VARCHAR(100))"
# # cmd = "SELECT * FROM api_keys;"
# # res = cursor.execute(cmd)
# # print(res.fetchone())
# # insert_api_key("1234")
# key = seek_api_key("1234")
# print(key)
# conn.close()


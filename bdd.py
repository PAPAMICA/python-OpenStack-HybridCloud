#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import openstack_api

def connect_to_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    return conn, cursor

def result_to_dict(dbresult):
    index = []
    for i in dbresult:
        index.append(i[0])
        index = list(set(index))

    result = {}
    for i in index:
        data = []
        for r in dbresult:
            if (r[0] == i):
                data.append(r[1])
        result[i] = data
    
    return result


def create_db_cloud(cloudname):
    try:
        conn, cursor = connect_to_db()
        conn.execute(f'''CREATE TABLE '{cloudname}'
                (TYPE           TEXT    NOT NULL,
                DATA           TEXT    NOT NULL);''')
        conn.close
        return (f"Table {cloudname} has been created")
    except:
        return (f"Table {cloudname} already exist")

def list_db_table():
    conn, cursor = connect_to_db()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    conn.close

def delete_db_table(table):
    conn, cursor = connect_to_db()
    cursor.execute(f"DROP TABLE {table}")
    conn.close

def insert_db_data(cloud_name, prout, data):
    conn, cursor = connect_to_db()
    for i in data:
        #sql = f'''INSERT INTO {cloud} (TYPE, DATA) VALUES ({type},{i})'''
        sql = f'''INSERT INTO {cloud_name} (TYPE, DATA) VALUES ("{prout}","{i}")'''
        conn.execute(sql)
        conn.commit()
        conn.close

def get_resources_list(cloud_name):
    try:
        conn, cursor = connect_to_db()
        sqlite_select_query = f"""SELECT * from {cloud_name}"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        conn.close
        result = result_to_dict(records)
        return result

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)


def fill_database(cloud_name):
    try:
        cloud = openstack_api.cloud_connection(cloud_name)
        data = openstack_api.list_flavors(cloud).values()
        insert_db_data(cloud_name, "FLAVOR", data)
        data = openstack_api.list_images(cloud).values()
        insert_db_data(cloud_name, "IMAGE", data)
        data = openstack_api.list_networks(cloud).values()
        insert_db_data(cloud_name, "NETWORK", data)
        data = openstack_api.list_keypairs(cloud).values()
        insert_db_data(cloud_name, "KEYPAIR", data)
        data = openstack_api.list_security_groups(cloud).values()
        insert_db_data(cloud_name, "SECURITY_GROUP", data)
        return ("SUCCESS")
    except:
        return ("ERROR")

def insert_api_key(key):
    conn, cursor = connect_to_db()
    query = f"INSERT INTO api_keys (key) VALUES('{key}');"
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
# #cmd = "CREATE TABLE api_keys(key VARCHAR(100))"
# cmd = "SELECT * FROM api_keys;"
# res = cursor.execute(cmd)
# # # # print(res.fetchone())
# # # # insert_api_key("1234")
# #key = seek_api_key("BTbKgc6HQCt92d7ym6m")
# print(res.fetchall())
# conn.close()


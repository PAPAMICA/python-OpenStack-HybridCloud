#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import api

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print ("Opened database successfully")

def create_db_cloud(cloudname):
    conn.execute(f'''CREATE TABLE '{cloudname}'
            (ID INT PRIMARY KEY     NOT NULL,
            DATE           TEXT    NOT NULL,
            IMAGES           TEXT    NOT NULL,
            NETWORKS           TEXT    NOT NULL,
            FLAVORS            TEXT     NOT NULL);''')
         
    print ("Table created successfully")

def list_db_table():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

def insert_db_data(cloud, type, data):
    conn.execute(f"INSERT INTO {cloud} ({type}) VALUES ({data})")
    conn.commit()



#create_db_cloud("Infomaniak")
#list_db_table()
insert_db_data("Infomaniak", "FLAVORS", data)
conn.close()


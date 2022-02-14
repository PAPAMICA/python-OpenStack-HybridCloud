#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import openstack_api

# from heatclient import client as _heatclient

# def heat_client(cloud):
#     return _heatclient.Client("1", session=cloud.session)
import subprocess
import os
import json

def connect_heat(cloud_name):

    file = f'/openrc/{cloud_name}'
    #file = '/Users/papamica/kDrive/ProjetsPerso/kubernetes/openrc'

    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            line=line.split()
            if len(line) > 1:
                word=line[1].split('=')
                globals()[word[0]] = word[1]
    os.putenv('OS_AUTH_URL', OS_AUTH_URL)
    os.putenv('OS_PROJECT_NAME', OS_PROJECT_NAME)  
    os.putenv('OS_USERNAME', OS_USERNAME)
    os.putenv('OS_PASSWORD', OS_PASSWORD)  
    os.putenv('OS_REGION_NAME', OS_REGION_NAME)   
    os.putenv('OS_PROJECT_DOMAIN_NAME', OS_PROJECT_DOMAIN_NAME)  
    os.putenv('OS_USER_DOMAIN_NAME', OS_USER_DOMAIN_NAME)  


def list_template():
    try:
        result = list()
        folder = os.listdir("heat_templates")
        for file in folder:
            result.append(file)
        return result
    except:
        print (f"[ERROR] Can't list templates !")



def deploy_app(cloud_name, template, app_name):
    try:
        connect_heat(cloud_name)
        result = dict()
        data = subprocess.getoutput(f'openstack stack create --wait -t heat_templates/{template} {app_name} 1> /dev/null && openstack stack show {app_name} -f json')
        result = json.loads(data)
        return result
    except:
        print (f"[ERROR] Can't deploy {app_name} !")

def get_info(cloud_name, app_name):
    try:
        connect_heat(cloud_name)
        result = dict()
        data = subprocess.getoutput(f'openstack stack show {app_name} -f json')
        result = json.loads(data)
        return result
    except:
        print (f"[ERROR] Can't get info of {app_name} !")

def delete_app(cloud_name, app_name):
    try:
        connect_heat(cloud_name)
        data = subprocess.getoutput(f'openstack stack delete {app_name}')
        return (f"[SUCCESS] {app_name} deleted !")
    except:
        print (f"[ERROR] Can't delete {app_name} !")

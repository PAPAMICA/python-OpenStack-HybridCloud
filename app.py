#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack
import openstack.exceptions
import os
import re
import json 

arg_json = 1

# Instance
instance_name = ""
instance_flavor = ""
instance_network= ""
instance_securitygroup = ""
instance_keypair = ""

# Others
cloud_name = "Infomaniak"
keypair_name = ""

# Connect to Openstack
def cloud_connection(cloud_name):
    if (cloud_name == "Infomaniak"):
        return openstack.connect(
            auth_url="https://api.pub1.infomaniak.cloud/identity/v3",
            project_name=os.getenv('OS_PROJECT_NAME'),
            username=os.getenv('OS_USERNAME'),
            password=os.getenv('OS_PASSWORD'),
            region_name="dc3-a",
            user_domain_name="default",
            project_domain_name="default",
            app_name='examples',
            app_version='1.0',
        )
    elif (cloud_name == "local"):
        print("Cloud selected : Local")

    else:
        print("Cloud selected ERROR")
        exit()

# Get all informations of all instances
def get_instances_list(cloud):
    total = ""
    for server in cloud.compute.servers():
        #print(server)
        secgroup = ""
        for i in server.security_groups:
            if (secgroup == ""):
                secgroup = i['name']
            else:
                secgroup = secgroup + ", " + i['name']
        image = cloud.compute.find_image(server.image.id)
        IPv4 = re.search(r'([0-9]{1,3}\.){3}[0-9]{1,3}', str(server.addresses))
        if arg_json == 1:
            data = {'instance': server.name}
            data['Cloud'] = cloud_name
            data['IP'] = IPv4.group()
            data['Keypair'] = server.key_name
            data['Image'] = image.name
            data['Flavor'] = server.flavor['original_name']
            data['Network'] = next(iter(server.addresses))
            data['Security_groups'] = secgroup
            data_json = json.dumps(data, indent = 4)
            total = total + data_json
        else:
            total = str(total) + f"{server.name}: \n  Cloud: {cloud_name}\n  IP: {IPv4.group()}\n  Keypair: {server.key_name} \n  Image: {image.name}\n  Network: {next(iter(server.addresses))} \n  Flavor: {server.flavor['original_name']} \n  Security_groups: {secgroup} \n "
    return total    
        
# Create Keypair
def create_keypair(cloud, keypair_name):
    keypair = cloud.compute.find_keypair(keypair_name)

    if not keypair:
        keypair = cloud.compute.create_keypair(name=keypair_name)
        if arg_json == 1:
            data = {'Private Key': keypair.private_key}
            return data
        else:
            return keypair.private_key
    else:
        print("This keypair already exist !")

# List networks
def list_networks(cloud):
    total = ""
    for network in cloud.network.networks():
        if arg_json == 1:
            data = {'network': network.name}
            data_json = json.dumps(data, indent = 4)
            total = total + data_json
        else:
            if (total == ""):
                total = network.name
            else:
                total = total + ", " + network.name

    return total

def list_images(cloud):
    total = ""
    for image in cloud.compute.images():
        if arg_json == 1:
            data = {'image': image.name}
            data_json = json.dumps(data, indent = 4)
            total = total + data_json
        else:
            if (total == ""):
                total = image.name
            else:
                total = total + ", " + image.name

    return total



cloud = cloud_connection(cloud_name)
#get_instances_list(cloud)
#create_keypair(cloud, keypair_name)
#list_networks(cloud)
print(list_images(cloud))
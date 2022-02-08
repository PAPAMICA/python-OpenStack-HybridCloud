#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack
import openstack.exceptions
import os
import re
import json 

arg_json = 0

# Instance
instance_name = ""
instance_flavor = ""
instance_network= ""
instance_securitygroup = ""
instance_keypair = ""

# Cloud
cloud_name = "Infomaniak"


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


def get_instances_list(cloud):
    total = ""
    for server in cloud.compute.servers():
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
            data['Image'] = image.name
            data['Flavor'] = server.flavor['original_name']
            data['Security_groups'] = secgroup
            data_json = json.dumps(data, indent = 4)
            total = total + data_json
        else:
            total = str(total) + f"{server.name}: \n  Cloud: {cloud_name}\n  IP: {IPv4.group()}\n  Image: {image.name}\n  Flavor: {server.flavor['original_name']} \n  Security_groups: {secgroup} \n "
    return total    
        

cloud = cloud_connection(cloud_name)
print(get_instances_list(cloud))
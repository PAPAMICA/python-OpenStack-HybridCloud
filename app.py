#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack
import openstack.exceptions
import os
import re
import json 

arg_json = 0

# Instance
instance_name = "test-name"
instance_image = "Debian 11.2 bullseye"
instance_flavor = "a1-ram2-disk20-perf1"
instance_network= "ext-net1"
instance_securitygroup = "ALLL"
instance_keypair = "Yubikey"

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
    result = ""
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
            result = result + data_json
        else:
            result = str(result) + f"{server.name}: \n  Cloud: {cloud_name}\n  IP: {IPv4.group()}\n  Keypair: {server.key_name} \n  Image: {image.name}\n  Network: {next(iter(server.addresses))} \n  Flavor: {server.flavor['original_name']} \n  Security_groups: {secgroup} \n "
    return result    
        
# Create Keypair
def create_keypair(cloud, keypair_name):
    keypair = cloud.compute.find_keypair(keypair_name)

    if not keypair:
        keypair = cloud.compute.create_keypair(name=keypair_name)
        if arg_json == 1:
            data = {'Private Key': keypair.private_key}
            return data
        else:
            print (keypair.private_key)
            return keypair
    else:
        return keypair

# List networks
def list_networks(cloud):
    result = ""
    for network in cloud.network.networks():
        if arg_json == 1:
            data = {'network': network.name}
            data_json = json.dumps(data, indent = 4)
            result = result + data_json
        else:
            if (result == ""):
                result = network.name
            else:
                result = result + ", " + network.name

    return result

# List security groups
def list_security_groups(cloud):
    result = ""
    for sc in cloud.network.security_groups():
        if arg_json == 1:
            data = {'security_group': sc.name}
            data['description'] = sc.description
            data_json = json.dumps(data, indent = 4)
            result = result + data_json
        else:
            if (result == ""):
                result = sc.name + " (" + sc.description + ")"
            else:
                result = result + ", " + sc.name + " (" + sc.description + ")"

    return result

# List images
def list_images(cloud):
    result = ""
    for image in cloud.compute.images():
        if arg_json == 1:
            data = {'image': image.name}
            data_json = json.dumps(data, indent = 4)
            result = result + data_json
        else:
            if (result == ""):
                result = image.name
            else:
                result = result + ", " + image.name

    return result

# List flavors
def list_flavors(cloud):
    result = ""
    for flavor in cloud.compute.flavors():
        if arg_json == 1:
            data = {'flavor': flavor.name}
            data_json = json.dumps(data, indent = 4)
            result = result + data_json
        else:
            if (result == ""):
                result = flavor.name
            else:
                result = result + ", " + flavor.name

    return result

# Create instance
def create_instance(cloud, instance_name,instance_image, instance_flavor, instance_network, instance_keypair, instance_securitygroup):
    result = ""
    image = cloud.compute.find_image(instance_image)
    flavor = cloud.compute.find_flavor(instance_flavor)
    network = cloud.network.find_network(instance_network)
    keypair = cloud.compute.find_keypair(instance_keypair)
    security_group = cloud.network.find_security_group(instance_securitygroup)

    server = cloud.compute.create_server(
        name=instance_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)

    server = cloud.compute.wait_for_server(server)
    server1 = cloud.compute.add_security_group_to_server(server, security_group)
    IPv4 = re.search(r'([0-9]{1,3}\.){3}[0-9]{1,3}', str(server.addresses))
    if arg_json == 1:
        data = {'instance': server.name}
        data['Cloud'] = cloud_name
        data['IP'] = IPv4.group()
        data['Keypair'] = server.key_name
        data['Image'] = image.name
        data['Flavor'] = server.flavor['original_name']
        data['Network'] = next(iter(server.addresses))
        data['Security_groups'] = instance_securitygroup
        result = json.dumps(data, indent = 4)
    else:
        result = str(result) + f"{server.name}: \n  Cloud: {cloud_name}\n  IP: {IPv4.group()}\n  Keypair: {server.key_name} \n  Image: {image.name}\n  Network: {next(iter(server.addresses))} \n  Flavor: {server.flavor['original_name']} \n  Security_groups: {instance_securitygroup} \n "
    return result



cloud = cloud_connection(cloud_name)
#get_instances_list(cloud)
#create_keypair(cloud, keypair_name)
#list_networks(cloud)
#list_security_groups(cloud)
#list_images(cloud)
#list_flavors(cloud))
print(create_instance(cloud, instance_name,instance_image, instance_flavor, instance_network, instance_keypair, instance_securitygroup))
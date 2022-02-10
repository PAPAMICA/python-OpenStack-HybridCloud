#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack
import openstack.exceptions
import os
import re
import json 
from flask import Flask, request, render_template, redirect
from jinja2 import Template

app = Flask(__name__)

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

@app.route("/", methods=['GET','POST'])
def hello():
    return render_template("index.html") #"Hello from Flask!"

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
        return redirect("http://192.168.2.53:9999")
        #print("Cloud selected : Local")

    else:
        print("Cloud selected ERROR")
        exit()


# Get all informations of all instances

#@app.route("/list", methods=['GET','POST'])
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
            data['Status'] = server.status
            data['IP'] = IPv4.group()
            data['Keypair'] = server.key_name
            data['Image'] = image.name
            data['Flavor'] = server.flavor['original_name']
            data['Network'] = next(iter(server.addresses))
            data['Security_groups'] = secgroup
            data_json = json.dumps(data, indent = 4)
            result = result + data_json
        else:
            result = str(result) + f"{server.name}: \n  Cloud: {cloud_name}\n  Status: {server.status}\n  IP: {IPv4.group()}\n  Keypair: {server.key_name} \n  Image: {image.name}\n  Network: {next(iter(server.addresses))} \n  Flavor: {server.flavor['original_name']} \n  Security_groups: {secgroup} \n "
    return result    

# Find and display information about one instance
@app.route("/get_instance_information")
def get_instance_information(cloud, server_name):
    try:
        result = ""
        server = cloud.compute.find_server(server_name)
        server = cloud.compute.get_server(server.id)
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
            data['Status'] = server.status
            data['IP'] = IPv4.group()
            data['Keypair'] = server.key_name
            data['Image'] = image.name
            data['Flavor'] = server.flavor['original_name']
            data['Network'] = next(iter(server.addresses))
            data['Security_groups'] = secgroup
            data_json = json.dumps(data, indent = 4)
            result = result + data_json
        else:
            result = str(result) + f"{server.name}: \n  Cloud: {cloud_name}\n  Status: {server.status}\n  IP: {IPv4.group()}\n  Keypair: {server.key_name} \n  Image: {image.name}\n  Network: {next(iter(server.addresses))} \n  Flavor: {server.flavor['original_name']} \n  Security_groups: {secgroup} \n "
        return result
    except:
        return (f"{server_name} not found !")


# Create Keypair
@app.route("/create_keypair")
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
@app.route("/list_networks")
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
@app.route("/list_security_groups")
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
@app.route("/list_images")
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
@app.route("/list_flavors")
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
@app.route("/create_server")
def create_instance(cloud, instance_name,instance_image, instance_flavor, instance_network, instance_keypair, instance_securitygroup):
    image = cloud.compute.find_image(instance_image)
    flavor = cloud.compute.find_flavor(instance_flavor)
    network = cloud.network.find_network(instance_network)
    keypair = cloud.compute.find_keypair(instance_keypair)
    security_group = cloud.network.find_security_group(instance_securitygroup)

    server = cloud.compute.create_server(
        name=instance_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)

    server = cloud.compute.wait_for_server(server)
    server = cloud.compute.add_security_group_to_server(server, security_group)
    print(get_instance_information(cloud, instance_name))


# Start instance
@app.route("/start_instance")
def start_instance(cloud, server_name):
    try:
        server = cloud.compute.find_server(server_name)
        server = cloud.compute. start_server(server.id)
        return f"[SUCCESS] {server_name} has been started !"
    except:
        return f"[ERROR] Can't start instance {server_name} !"

# Stop instance
@app.route("/stop_instance")
def stop_instance(cloud, server_name):
    try:
        server = cloud.compute.find_server(server_name)
        server = cloud.compute. stop_server(server.id)
        return f"[SUCCESS] {server_name} has been stopped !"
    except:
        return f"[ERROR] Can't stop instance {server_name} !"

# Reboot instance
@app.route("/reboot_instance")
def reboot_instance(cloud, server_name):
    try:
        server = cloud.compute.find_server(server_name)
        server = cloud.compute. reboot_server(server.id, "HARD")
        return f"[SUCCESS] {server_name} has been rebooted !"
    except:
        return f"[ERROR] Can't reboot instance {server_name} !"

# Delete instance
@app.route("/delete_instance")
def delete_instance(cloud, server_name):
    try:
        server = cloud.compute.find_server(server_name)
        server = cloud.compute. delete_server(server.id)
        return f"[SUCCESS] {server_name} has been deleted !"
    except:
        return f"[ERROR] Can't delete instance {server_name} !"


#cloud = cloud_connection(cloud_name)
#result = get_instances_list(cloud)
if __name__ == '__main__':
    app.run(host="192.168.2.53", port=8085, debug=False)
#get_instances_list(cloud)
#get_instance_information(cloud, server_name)
#create_keypair(cloud, keypair_name)
#list_networks(cloud)
#list_security_groups(cloud)
#list_images(cloud)
#list_flavors(cloud))
#create_instance(cloud, instance_name,instance_image, instance_flavor, instance_network, instance_keypair, instance_securitygroup)
#stop_instance(cloud, server_name)
#start_instance(cloud, server_name)
#reboot_instance(cloud, server_name)
#delete_instance(cloud, server_name)

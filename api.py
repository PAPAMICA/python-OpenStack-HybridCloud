from __main__ import app
from unittest import result
import openstack_api
from flask import Flask, request, render_template, redirect

@app.route("/api/list/<cloud_name>", methods=['GET'])
def display_instances_list(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.get_instances_list(cloud)
    return result

@app.route("/api/<cloud_name>/<server_name>", methods=['GET','DELETE'])
def display_instance_information(cloud_name,server_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    if request.method == 'GET':
        result = openstack_api.get_instance_information(cloud, server_name)
    elif request.method == 'DELETE':
        result = openstack_api.delete_instance(cloud, server_name)
    return result

@app.route("/api/<cloud_name>/new_keypair", methods=['POST'])
def create_keypair(cloud_name):
    data = request.json
    keypair_name = data['keypair_name']
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.create_keypair(cloud, keypair_name)
    return result

@app.route("/api/<cloud_name>/networks", methods=['GET'])
def display_networks(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.list_networks(cloud)
    return result

@app.route("/api/<cloud_name>/security_groups", methods=['GET'])
def display_security_groups(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.list_security_groups(cloud)
    return result

@app.route("/api/<cloud_name>/images", methods=['GET'])
def display_images(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.list_images(cloud)
    return result

@app.route("/api/<cloud_name>/flavors", methods=['GET'])
def display_flavors(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.list_flavors(cloud)
    return result

@app.route("/api/<cloud_name>/new_instance", methods=['POST'])
def create_instance(cloud_name):
    data = request.json
    instance_name    = data['instance_name']
    instance_image   = data['instance_image']
    instance_flavor  = data['instance_flavor']
    instance_network = data['instance_network']
    instance_keypair = data['instance_keypair']
    instance_securitygroup = data['instance_securitygroup']
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.create_instance(cloud, instance_name,instance_image, instance_flavor, instance_network, instance_keypair, instance_securitygroup)
    return result

@app.route("/api/<cloud_name>/<server_name>/start", methods=['GET'])
def start_instance(cloud_name, server_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.start_instance(cloud, server_name)
    return result

@app.route("/api/<cloud_name>/<server_name>/stop", methods=['GET'])
def stop_instance(cloud_name, server_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.stop_instance(cloud, server_name)
    return result

@app.route("/api/<cloud_name>/<server_name>/reboot", methods=['GET'])
def reboot_instance(cloud_name, server_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.reboot_instance(cloud, server_name)
    return result

# @app.route("/api/<cloud_name>/<server_name>/delete", methods=['GET'])
# def delete_instance(cloud_name, server_name):
#     cloud  = openstack_api.cloud_connection(cloud_name)
#     result = openstack_api.delete_instance(cloud, server_name)
#     return result
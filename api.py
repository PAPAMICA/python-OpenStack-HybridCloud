from __main__ import app
from unittest import result
import openstack_api
from flask import Flask, request, render_template, redirect

@app.route("/api/list/<cloud_name>", methods=['GET','POST'])
def display_instances_list(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.get_instances_list(cloud)
    return result

@app.route("/api/list/<cloud_name>/<server_name>")
def display_instance_information(cloud_name,server_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.get_instance_information(cloud, server_name)
    return result

@app.route("/api/<cloud_name>/new_keypair")
def create_keypair(cloud_name):
    keypair_name = request.headers['keypair_name']
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.create_keypair(cloud, keypair_name)
    return result

@app.route("/api/<cloud_name>/networks")
def display_networks(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.list_networks(cloud)
    return result

@app.route("/api/<cloud_name>/security_groups")
def display_security_groups(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.list_security_groups(cloud)
    return result

@app.route("/api/<cloud_name>/images")
def display_images(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.list_images(cloud)
    return result

@app.route("/api/<cloud_name>/flavors")
def display_flavors(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.list_flavors(cloud)
    return result

@app.route("/api/<cloud_name>/new_instance")
def create_instance(cloud_name):
    instance_name    = request.headers['instance_name']
    instance_image   = request.headers['instance_image']
    instance_flavor  = request.headers['instance_flavor']
    instance_network = request.headers['instance_network']
    instance_keypair = request.headers['instance_keypair']
    instance_securitygroup = request.headers['instance_securitygroup']
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.create_instance(cloud, instance_name,instance_image, instance_flavor, instance_network, instance_keypair, instance_securitygroup)
    return result

@app.route("/api/<cloud_name>/<server_name>/start")
def start_instance(cloud_name, server_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = start_instance(cloud, server_name)
    return result

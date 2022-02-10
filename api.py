from __main__ import app
import openstack_api
from flask import Flask, request, render_template, redirect

@app.route("/api/list/<cloud_name>", methods=['GET','POST'])
def display_instances_list(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.get_instances_list(cloud)
    return(result)

@app.route("/api/inst_info/<cloud_name>/<server_name>")
def display_instance_information(cloud_name,server_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.get_instance_information(cloud, server_name)
    return(result)
from __main__ import app
from unittest import result
import openstack_api
import rating_api
from flask import Flask, Response, request, render_template, redirect, jsonify
import bdd
import sys
import json

@app.route("/api/list/instances/<cloud_name>", methods=['GET'])
def display_instances_list(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.get_instances_list(cloud)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/list/resources/<cloud_name>", methods=['GET'])
def display_resources_list(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        result = bdd.get_resources_list(cloud_name)
        if result == None:
            update_resources_list(cloud_name)
            display_resources_list(cloud_name)
            return result,200
        else:
            return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/update/resources/<cloud_name>", methods=['GET'])
def update_resources_list(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        try:
            delete = bdd.delete_db_table(cloud_name)
        except:
            pass
        table = bdd.create_db_cloud(cloud_name)
        result = bdd.fill_database(cloud_name)
        print(result, flush=True, file=sys.stdout)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/<server_name>", methods=['GET','DELETE'])
def display_instance_information(cloud_name,server_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        if request.method == 'GET':
            result = openstack_api.get_instance_information(cloud, server_name)
        elif request.method == 'DELETE':
            result = openstack_api.delete_instance(cloud, server_name)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/new_keypair", methods=['POST'])
def create_keypair(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        data = request.json
        keypair_name = data['keypair_name']
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.create_keypair(cloud, keypair_name)
        json_result = json.dumps(result)
        return Response(json_result,status=201)
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/networks", methods=['GET'])
def display_networks(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.list_networks(cloud)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/keypairs", methods=['GET'])
def display_keypairs(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.list_keypairs(cloud)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/security_groups", methods=['GET'])
def display_security_groups(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.list_security_groups(cloud)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/images", methods=['GET'])
def display_images(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.list_images(cloud)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/flavors", methods=['GET'])
def display_flavors(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.list_flavors(cloud)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/new_instance", methods=['POST'])
def create_instance(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        data = request.json
        print(f"data here : {data}", flush=True, file=sys.stdout)
        instance_name    = data['instance_name']
        instance_image   = data['instance_image']
        instance_flavor  = data['instance_flavor']
        instance_network = data['instance_network']
        instance_keypair = data['instance_keypair']
        instance_securitygroup = data['instance_securitygroup']
        cloud  = openstack_api.cloud_connection(cloud_name)
        openstack_api.create_instance(cloud, instance_name,instance_image, instance_flavor, instance_network, instance_keypair, instance_securitygroup)
        return Response("201 : success", status=201)
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/<server_name>/start", methods=['GET'])
def start_instance(cloud_name, server_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.start_instance(cloud, server_name)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/<server_name>/stop", methods=['GET'])
def stop_instance(cloud_name, server_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.stop_instance(cloud, server_name)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/<server_name>/reboot", methods=['GET'])
def reboot_instance(cloud_name, server_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        cloud  = openstack_api.cloud_connection(cloud_name)
        result = openstack_api.reboot_instance(cloud, server_name)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

@app.route("/api/<cloud_name>/billing", methods=['GET'])
def get_billing(cloud_name):
    api_key = request.args.get('api_key')
    res = bdd.seek_api_key(api_key)
    if res:
        result = rating_api.get_billing(cloud_name)
        return result,200
    else:
        return Response("403 : Access denied",status=403)

from email import header
from re import A
import requests
import json
import ast
from flask import Flask, flash, request, render_template, redirect
app = Flask(__name__)
app.secret_key = b'_5#y2L"342F4Q8z\n\xec]/'
import api
import openstack_api
import sys
import time
import bdd
import random
import string
import rating_api
import heat_api


dashbord_url = "https://hybridcloud.papamica.com"
global billingG

@app.route("/", methods=['GET','POST'])
def home():
    result = dict()
    cloud_name = str()
    api_key = ""
    key_name = ""
    billing = billingG
    if request.method == 'POST':
        if request.form.get('instance_start'):
            instance_name = request.form['instance_start']
            cloud_name = request.form['cloud_name']
            cloud  = openstack_api.cloud_connection(cloud_name)
            openstack_api.start_instance(cloud, instance_name)
            time.sleep(5)
            result = reload_list(cloud_name)
        elif request.form.get('instance_reboot'):
            instance_name = request.form['instance_reboot']
            cloud_name = request.form['cloud_name']
            cloud  = openstack_api.cloud_connection(cloud_name)
            result = openstack_api.reboot_instance(cloud, instance_name)
            time.sleep(5)
            result = reload_list(cloud_name)

        elif request.form.get('instance_stop'):
            instance_name = request.form['instance_stop']
            cloud_name = request.form['cloud_name']
            cloud  = openstack_api.cloud_connection(cloud_name)
            result = openstack_api.stop_instance(cloud, instance_name)
            time.sleep(5)
            result = reload_list(cloud_name)

        elif request.form.get('instance_destroy'):
            instance_name = request.form['instance_destroy']
            cloud_name = request.form['cloud_name']
            cloud  = openstack_api.cloud_connection(cloud_name)
            result = openstack_api.delete_instance(cloud, instance_name)
            time.sleep(5)
            result = reload_list(cloud_name)

        elif request.form.get('app_destroy'):
            app_list = dict()
            app_name = request.form['app_destroy']
            cloud_name = request.form['cloud_name']
            result = heat_api.delete_app(cloud_name, app_name)
            time.sleep(5)
            app_list[cloud_name] = heat_api.list_app(cloud_name)
            return render_template("index.html", applications=app_list, cloud_name=cloud_name, billing=billing)


        elif request.form.get('app_information'):
            app_list = dict()
            app_name = request.form['app_information']
            cloud_name = request.form['cloud_name']
            result = heat_api.get_info(cloud_name, app_name)
            app_list[cloud_name] = heat_api.list_app(cloud_name)
            return render_template("index.html", applications=app_list, app_informations=result, cloud_name=cloud_name, billing=billing)

        elif request.form.get('list_apikey'):
            result = bdd.list_api_key()
            print(result, flush=True, file=sys.stdout)
            return render_template("index.html", list_api_key=result, billing=billing)

        elif request.form.get('get_apikey'):
            key_name = request.form['key_name']
            characters = string.ascii_letters + string.digits
            api_key = ''.join(random.choice(characters) for i in range(18))
            bdd.insert_api_key(api_key,key_name)
            return render_template("index.html", api_key=api_key, key_name = key_name, billing=billing)
        
        elif request.form.get('delete_apikey'):
            key_name = request.form['delete_apikey']
            bdd.delete_api_key(key_name)
            result = bdd.list_api_key()
            return render_template("index.html", list_api_key=result, billing=billing)
        
        
        elif request.form.get('create_instance'):
            cloud = ['Infomaniak', 'Local']
            result = {}   
            for cloud_name in cloud:
                result[cloud_name] = bdd.get_resources_list(cloud_name)
            return render_template("create_instance.html",resources=result, cloud_name=cloud_name)

        elif request.form.get('create_instance_2'):
            cloud_name = request.form['cloud_name']
            instance_name = request.form['iname']
            instance_flavor = request.form['FLAVOR']
            instance_keypair = request.form['KEYPAIR']
            instance_image = request.form['IMAGE']
            instance_network = request.form['NETWORK']
            instance_sc = request.form['SECURITY_GROUP']
            cloud  = openstack_api.cloud_connection(cloud_name)
            openstack_api.create_instance(cloud, instance_name,instance_image, instance_flavor, instance_network, instance_keypair, instance_sc)

        elif request.form.get('deploy_app'):
            clouds = ['Infomaniak', 'Local']
            templates = heat_api.list_template(clouds)
            return render_template("deploy_app.html",clouds=clouds, templates=templates)

        elif request.form.get('deploy_app_2'):
            cloud_name = request.form['cloud_name']
            app_name = request.form['aname']
            template = request.form['template']
            result = heat_api.deploy_app(cloud_name, template, app_name)
            return render_template("deploy_app.html",result=result, cloud_name=cloud_name)
            
        elif request.form.get('refresh-billing'):
            result = {}  
            billing = rating_api.get_billing("Infomaniak")
            return render_template("index.html",billing=billing), billing

        elif request.form.get('list_resources'):
            cloud = request.form.getlist('cloud')
            result = {}   
            for cloud_name in cloud:
                result[cloud_name] = bdd.get_resources_list(cloud_name)
            return render_template("index.html",resources=result, cloud_name=cloud_name, billing=billing)

        elif request.form.get('update_resources'):
            cloud = request.form.getlist('cloud')
            result = {}   
            for cloud_name in cloud:
                bdd.delete_db_table(cloud_name)
                bdd.create_db_cloud(cloud_name)
                bdd.fill_database(cloud_name)
                result[cloud_name] = bdd.get_resources_list(cloud_name)
            print(result, flush=True, file=sys.stdout)
            return render_template("index.html",resources=result, cloud_name=cloud_name, billing=billing)

        elif request.form.get('list_applications'):
            cloud = request.form.getlist('cloud')
            result = {}   
            for cloud_name in cloud:
                result[cloud_name] = heat_api.list_app(cloud_name)
            print(result, flush=True, file=sys.stdout)
            return render_template("index.html",applications=result, cloud_name=cloud_name, billing=billing)

        elif request.form.get('list_instances'):
            cloud = request.form.getlist('cloud')
            result = {}   
            for cloud_name in cloud:
                cloud_connect  = openstack_api.cloud_connection(cloud_name)
                result[cloud_name] = openstack_api.get_instances_list(cloud_connect)
            print(result, flush=True, file=sys.stdout)
    return render_template("index.html",instances=result, cloud_name=cloud_name, billing=billing)


def reload_list(cloud_name):
    result = dict()
    cloud_connect  = openstack_api.cloud_connection(cloud_name)
    result[cloud_name] = openstack_api.get_instances_list(cloud_connect)
    return result

if __name__ == "__main__":
    table = bdd.create_db_cloud("Infomaniak")
    result = bdd.fill_database("Infomaniak")
    print(result, flush=True, file=sys.stdout)
    table = bdd.create_db_cloud("Local")
    result = bdd.fill_database("Local")
    print(result, flush=True, file=sys.stdout)
    billingG = rating_api.get_billing("Infomaniak")
    app.run(host="0.0.0.0", port="8086", debug=False)
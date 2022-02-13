from email import header
from re import A
import requests
import json
import ast
from flask import Flask, request, render_template, redirect
app = Flask(__name__)
import api
import sys
import time
import bdd
import random
import string
import rating_api


dashbord_url = "https://hybridcloud.papamica.com"

@app.route("/", methods=['GET','POST'])
def home():
    result = dict()
    cloud_name = str()
    api_key = ""
    key_name = ""
    if request.method == 'POST':
        if request.form.get('start'):
            instance_name = request.form.getlist('start')
            cloud_name = request.form.getlist('cloud_name')
            url = f'{dashbord_url}/api/{cloud_name[0]}/{instance_name[0]}/start?api_key=1234'
            result = requests.get(url)
            #print(result, flush=True, file=sys.stdout)
            time.sleep(2)
            data = reload_list(cloud_name[0])
        elif request.form.get('reboot'):
            instance_name = request.form.getlist('reboot')
            cloud_name = request.form.getlist('cloud_name')
            url = f'{dashbord_url}/api/{cloud_name[0]}/{instance_name[0]}/reboot?api_key=1234'
            result = requests.get(url)
            #print(result, flush=True, file=sys.stdout)
            time.sleep(1)
            data = reload_list(cloud_name[0])
        elif request.form.get('stop'):
            instance_name = request.form.getlist('stop')
            cloud_name = request.form.getlist('cloud_name')
            url = f'{dashbord_url}/api/{cloud_name[0]}/{instance_name[0]}/stop?api_key=1234'
            result = requests.get(url)
            #print(result, flush=True, file=sys.stdout)
            time.sleep(2)
            data = reload_list(cloud_name[0])
        elif request.form.get('destroy'):
            instance_name = request.form['destroy']
            cloud_name = request.form.getlist('cloud_name')
            url = f'{dashbord_url}/api/{cloud_name[0]}/{instance_name}?api_key=1234'
            result = requests.delete(url)
            #print(result, flush=True, file=sys.stdout)
            time.sleep(3)
            data = reload_list(cloud_name[0])


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
            key_name = request.form['key_name']
            bdd.delete_api_key(key_name)
        
        
        elif request.form.get('create_instance'):
            cloud = request.form.getlist('cloud')
            cloud_name = cloud[0]
            url = f'{dashbord_url}/api/list/resources/{cloud_name}?api_key=1234'
            data = requests.get(url,verify=True)
            data = data.content
            data = json.loads(data.decode('utf-8'))
            result[cloud_name] = data
            return render_template("create.html",resources=result, cloud_name=cloud_name, billing=billing)

        elif request.form.get('create_instance_2'):
            cloud_name = request.form['cloud_name']
            instance_name = request.form['iname']
            instance_flavor = request.form['FLAVOR']
            instance_image = request.form['IMAGE']
            instance_keypair = request.form['KEYPAIR']
            instance_network = request.form['NETWORK']
            instance_sc = request.form['SECURITY_GROUP']
            headers = {"Content-Type":"application/json"}
            body = {       
                        "instance_name":instance_name,
                        "instance_image":instance_image,
                        "instance_flavor":instance_flavor,
                        "instance_network":instance_network,
                        "instance_keypair":instance_keypair,
                        "instance_securitygroup":instance_sc
                    }
            url = f'{dashbord_url}/api/{cloud_name}/new_instance?api_key=1234'
            r = requests.post(url,data=json.dumps(body),headers=headers,verify=True)
            print(r, json.dumps(body)) 
            #data = data.content
            #data = json.loads(data.decode('utf-8'))
            #result[cloud_name] = data
            #return render_template("create.html",resources=result, cloud_name=cloud_name)
            
        elif request.form.get('refresh-billing'):
            result = {}  
            global billing
            #url = f'{dashbord_url}/api/Infomaniak/billing?api_key=1234'
            #data = requests.get(url,verify=True)
            #data = data.content
            #billing = json.loads(data.decode('utf-8'))
            billing = rating_api.get_billing("Infomaniak")
            return render_template("index.html",billing=billing)

        elif request.form.get('list_resources'):
            cloud = request.form.getlist('cloud')
            result = {}   
            for cloud_name in cloud:
                url = f'{dashbord_url}/api/list/resources/{cloud_name}?api_key=1234'
                #url = f'{dashbord_url}/api/list/resources/Infomaniak?api_key=1234'
                data = requests.get(url,verify=True)
                data = data.content
                data = json.loads(data.decode('utf-8'))
                result[cloud_name] = data
            return render_template("index.html",resources=result, cloud_name=cloud_name, billing=billing)

        elif request.form.get('update_resources'):
            cloud = request.form.getlist('cloud')

            result = {}   
            for cloud_name in cloud:
                url = f'{dashbord_url}/api/update/resources/{cloud_name}?api_key=1234'
                #url = f'{dashbord_url}/api/update/resources/Infomaniak?api_key=1234'
                update = requests.get(url,verify=True)
                url = f'{dashbord_url}/api/list/resources/{cloud_name}?api_key=1234'
                #url = f'{dashbord_url}/api/list/resources/Infomaniak?api_key=1234'
                data = requests.get(url,verify=True)
                data = data.content
                data = json.loads(data.decode('utf-8'))
                result[cloud_name] = data
            print(result, flush=True, file=sys.stdout)
            return render_template("index.html",resources=result, cloud_name=cloud_name, billing=billing)

        elif request.form.get('list_instances'):
            cloud = request.form.getlist('cloud')
            result = {}   
            for cloud_name in cloud:
                url = f'{dashbord_url}/api/list/instances/{cloud_name}?api_key=1234'
                #url = f'{dashbord_url}/api/list/instances/Infomaniak?api_key=1234'
                data = requests.get(url,verify=True)
                print(data, flush=True, file=sys.stdout)
                data = data.content
                data = json.loads(data.decode('utf-8'))
                result[cloud_name] = data
            print(result, flush=True, file=sys.stdout)
            #return render_template("index.html",instances=data, cloud_name=cloud_name)
    return render_template("index.html",instances=result, cloud_name=cloud_name, billing=billing)


def reload_list(cloud_name):
    url = f'{dashbord_url}/api/list/instances/{cloud_name}?api_key=1234'
    result = requests.get(url,verify=True)
    data = result.content
    data = json.loads(data.decode('utf-8'))
    return data


# @app.route("/list", methods=['GET','POST'])
# def web_list_instances():
#     cloud_name = request.form["cloud"]
#     url = f'{dashbord_url}/api/list/{cloud_name}'
#     result = requests.get(url,verify=True)
#     return result.content

if __name__ == "__main__":
    table = bdd.create_db_cloud("Infomaniak")
    result = bdd.fill_database("Infomaniak")
    print(result, flush=True, file=sys.stdout)
    table = bdd.create_db_cloud("Local")
    result = bdd.fill_database("Local")
    print(result, flush=True, file=sys.stdout)
    billing = rating_api.get_billing("Infomaniak")
    print(billing, flush=True, file=sys.stdout)
    app.run(host="0.0.0.0", port="8086", debug=True)
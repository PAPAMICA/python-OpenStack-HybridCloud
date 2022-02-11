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


dashbord_url = "https://hybridcloud.papamica.com"

@app.route("/", methods=['GET','POST'])
def home():
    data = dict()
    cloud_name = str()
    if request.method == 'POST':
        if request.form.get('start'):
            instance_name = request.form.getlist('start')
            cloud_name = request.form.getlist('cloud_name')
            url = f'{dashbord_url}/api/{cloud_name[0]}/{instance_name[0]}/start'
            result = requests.get(url)
            #print(result, flush=True, file=sys.stdout)
            time.sleep(2)
            data = reload_list(cloud_name[0])
        elif request.form.get('reboot'):
            instance_name = request.form.getlist('reboot')
            cloud_name = request.form.getlist('cloud_name')
            url = f'{dashbord_url}/api/{cloud_name[0]}/{instance_name[0]}/reboot'
            result = requests.get(url)
            #print(result, flush=True, file=sys.stdout)
            time.sleep(1)
            data = reload_list(cloud_name[0])
        elif request.form.get('stop'):
            instance_name = request.form.getlist('stop')
            cloud_name = request.form.getlist('cloud_name')
            url = f'{dashbord_url}/api/{cloud_name[0]}/{instance_name[0]}/stop'
            result = requests.get(url)
            #print(result, flush=True, file=sys.stdout)
            time.sleep(2)
            data = reload_list(cloud_name[0])
        elif request.form.get('destroy'):
            instance_name = request.form.getlist('destroy')
            cloud_name = request.form.getlist('cloud_name')
            url = f'{dashbord_url}/api/{cloud_name[0]}/{instance_name[0]}'
            result = requests.delete(url)
            #print(result, flush=True, file=sys.stdout)
            time.sleep(1)
            data = reload_list(cloud_name[0])


        elif request.form.get('get-apikey'):
            print("jsuispasséICI", flush=True, file=sys.stdout)
            characters = string.ascii_letters + string.digits
            api_key = ''.join(random.choice(characters) for i in range(18))
            bdd.insert_api_key(api_key)
            return render_template("index.html", api_key=api_key)
        
        elif request.form.get('create_instance'):
            cloud_name = request.form.getlist('cloud')
            if cloud_name:
                cloud_name = "Infomaniak"
            else:
                cloud_name = "local"
            url = f'{dashbord_url}/api/list/instances/{cloud_name}?api_key=1234'
            result = requests.get(url,verify=True)
            data = result.content
            data = json.loads(data.decode('utf-8'))
            if data == None:
                data = {}   

        elif request.form.get('list_instance'):
            cloud_name = request.form.getlist('cloud')
            if cloud_name:
                cloud_name = "Infomaniak"
            else:
                cloud_name = "local"
            url = f'{dashbord_url}/api/list/instances/{cloud_name}?api_key=1234'
            print(cloud_name, flush=True, file=sys.stdout)
            result = requests.get(url,verify=True)
            data = result.content
            data = json.loads(data.decode('utf-8'))
            if data == None:
                data = {}   
            #return render_template("index.html",instances=data, cloud_name=cloud_name)
    return render_template("index.html",instances=data, cloud_name=cloud_name)

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
    app.run(host="0.0.0.0", port="8086", debug=True)
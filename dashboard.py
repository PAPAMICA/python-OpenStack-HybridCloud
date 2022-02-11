import requests
import json
import ast
from flask import Flask, request, render_template, redirect
app = Flask(__name__)
import api
import sys


dashbord_url = "https://hybridcloud.papamica.com"

@app.route("/", methods=['GET','POST'])
def home():
    data = dict()
    if request.method == 'POST':
        if request.form.get('cloud'):
            cloud_name = request.form.getlist('cloud')
            if cloud_name:
                cloud_name = "Infomaniak"
            else:
                cloud_name = "local"
            url = f'{dashbord_url}/api/list/{cloud_name}'
            result = requests.get(url,verify=True)
            data = result.content
            data = json.loads(data.decode('utf-8'))
            if data == None:
                data = {}   
            return render_template("index.html",instances=data, cloud_name=cloud_name)

        elif request.form.get('start'):
            instance_name = request.form.getlist('start')
            cloud_name = request.form.getlist('cloud_name')
            url = f'{dashbord_url}/api/{cloud_name[0]}/{instance_name[0]}/start'
            print(url, flush=True, file=sys.stdout)
            result = requests.get(url,verify=True)
            print(result, flush=True, file=sys.stdout)
            reload_list(cloud_name)
    return render_template("index.html")

def reload_list(cloud_name):
    url = f'{dashbord_url}/api/list/{cloud_name}'
    result = requests.get(url,verify=True)
    data = result.content
    data = json.loads(data.decode('utf-8'))
    if data == None:
        data = {}   
    return render_template("index.html",instances=data, cloud_name=cloud_name)


# @app.route("/list", methods=['GET','POST'])
# def web_list_instances():
#     cloud_name = request.form["cloud"]
#     url = f'{dashbord_url}/api/list/{cloud_name}'
#     result = requests.get(url,verify=True)
#     return result.content

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8086", debug=True)
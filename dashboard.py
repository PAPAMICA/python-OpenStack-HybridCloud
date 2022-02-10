import requests
import json
import ast
from flask import Flask, request, render_template, redirect
app = Flask(__name__)
import api

dashbord_url = "https://hybridcloud.papamica.com"

@app.route("/", methods=['GET','POST'])
def list_instances():
    data = dict()
    if request.method == 'POST':
        if request.form['cloud']:
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
        if request.form['start']:
            instance_name = request.form.getlist('start')
    return render_template("index.html",instances=data)

# @app.route("/list", methods=['GET','POST'])
# def web_list_instances():
#     cloud_name = request.form["cloud"]
#     url = f'{dashbord_url}/api/list/{cloud_name}'
#     result = requests.get(url,verify=True)
#     return result.content

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8086", debug=True)
import requests
import json
from flask import Flask, request, render_template, redirect
app = Flask(__name__)
import api

dashbord_url = "https://hybridcloud.papamica.com"

@app.route("/", methods=['GET','POST'])
def hello():
    test = dict()
    if request.method == 'POST':
        cloud_name = request.form["cloud"]
        url = f'{dashbord_url}/api/list/{cloud_name}'
        result = requests.get(url,verify=True)
        data = result.content
        data = data.decode('utf8').replace("'", '"')
        data = json.loads(data)
        result = json.dumps(data, indent=4, sort_keys=True)
        # if test == None:
        #     test = {}   
    return render_template("index.html",instances=result)

# @app.route("/list", methods=['GET','POST'])
# def web_list_instances():
#     cloud_name = request.form["cloud"]
#     url = f'{dashbord_url}/api/list/{cloud_name}'
#     result = requests.get(url,verify=True)
#     return result.content

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8086", debug=True)
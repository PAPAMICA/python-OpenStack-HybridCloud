import dashboard_copy
import requests
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello():
    return render_template("index.html")

@app.route("/list/", methods=['GET','POST'])
def web_list_instances():
    cloud_name = request.form["cloud"]
    url = f'http://192.168.2.53:8086/api/list/{cloud_name}'
    result = requests.get(url)
    return result.content
    

@app.route("/api/list/<cloud_name>", methods=['GET','POST'])
def display_instances_list(cloud_name):
    cloud = dashboard_copy.cloud_connection(cloud_name)
    result = dashboard_copy.get_instances_list(cloud)
    return(result)

if __name__ == "__main__":
    app.run(host="192.168.2.53", port=8086, debug=False)
    #app.run(host="192.168.2.53", port=8086, debug=False)

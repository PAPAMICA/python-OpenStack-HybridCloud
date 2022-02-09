import api
from flask import Flask, request, render_template, redirect, jsonify

dashboard_ip = "0.0.0.0"

app = Flask(__name__)


@app.route("/list", methods=['GET','POST'])
def display_instances_list():
    cloud_name = request.form['cloud']
    cloud = api.cloud_connection(cloud_name)
    result = api.get_instances_list(cloud)
    return result


@app.route("/", methods=['GET','POST'])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host=dashboard_ip, port=8086, debug=True)
    
import api
import requests
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
dashbord_url = "10.10.0.108"

@app.route("/", methods=['GET','POST'])
def hello():
    return render_template("index.html")

@app.route("/list/", methods=['GET','POST'])
def web_list_instances():
    cloud_name = request.form["cloud"]
    url = f'http://{dashbord_url}:8086/api/list/{cloud_name}'
    result = requests.get(url)
    return result.content

if __name__ == "__main__":
    app.run(host=dashbord_url, port=8085, debug=True)
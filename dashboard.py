import requests
from flask import Flask, request, render_template, redirect
app = Flask(__name__)
import api

dashbord_url = "https://hybridcloud.papamica.com"

@app.route("/", methods=['GET','POST'])
def hello():
    test = False
    if request.method == 'POST':
        cloud_name = request.form["cloud"]
        url = f'{dashbord_url}/api/list/{cloud_name}'
        result = requests.get(url,verify=True)
    return render_template("index.html",test=result.content)

# @app.route("/list", methods=['GET','POST'])
# def web_list_instances():
#     cloud_name = request.form["cloud"]
#     url = f'{dashbord_url}/api/list/{cloud_name}'
#     result = requests.get(url,verify=True)
#     return result.content

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8086", debug=True)
import openstack_api
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
dashbord_url = "0.0.0.0"

@app.route("/api/list/<cloud_name>", methods=['GET','POST'])
def display_instances_list(cloud_name):
    cloud  = openstack_api.cloud_connection(cloud_name)
    result = openstack_api.get_instances_list(cloud)
    return(result)

if __name__ == "__main__":
    app.run(host=dashbord_url, port=8086, debug=True)
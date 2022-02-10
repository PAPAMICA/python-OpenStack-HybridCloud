import openstack_functions
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route("/api/list/<cloud_name>", methods=['GET','POST'])
def display_instances_list(cloud_name):
    cloud  = openstack_functions.cloud_connection(cloud_name)
    result = openstack_functions.get_instances_list(cloud)
    return(result)

if __name__ == "__main__":
    app.run(host="192.168.2.53", port=8086, debug=False)

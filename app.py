#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack
import openstack.exceptions
import os


# Instance
instance_name = ""
instance_flavor = ""
instance_network= ""
instance_securitygroup = ""
instance_keypair = ""

# Cloud
cloud_name = "Infomaniak"


def cloud_connection(cloud_name):
    if (cloud_name == "Infomaniak"):
        return openstack.connect(
            auth_url="https://api.pub1.infomaniak.cloud/identity/v3",
            project_name=os.getenv('OS_PROJECT_NAME'),
            username=os.getenv('OS_USERNAME'),
            password=os.getenv('OS_PASSWORD'),
            region_name="dc3-a",
            user_domain_name="default",
            project_domain_name="default",
            app_name='examples',
            app_version='1.0',
        )
    elif (cloud_name == "local"):
        print("Cloud selected : Local")

    else:
        print("Cloud selected ERROR")
        exit()


def get_instances_list(cloud):
     for server in cloud.compute.servers():
         print(server)


cloud = cloud_connection(cloud_name)
get_instances_list(cloud)
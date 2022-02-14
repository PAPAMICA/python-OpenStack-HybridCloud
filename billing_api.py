#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack_api

from cloudkittyclient import client as _cloudkittyclient

def cloudkitty_client(cloud):
    return _cloudkittyclient.Client("1", session=cloud.session)


def project_dataframes(cloud, tenant_id, begin, end):

    cloudkitty = cloudkitty_client(cloud)
    dataframes_raw = cloudkitty.storage.get_dataframes(
        tenant_id=tenant_id, begin=begin, end=end
    )["dataframes"]

    for dataframe_raw in dataframes_raw:
        for resource in dataframe_raw["resources"]:
            rating = float(resource["rating"])
            if rating == 0:
                continue

            dataframe = {}
            dataframe["begin"] = dataframe_raw["begin"]
            dataframe["end"] = dataframe_raw["end"]
            dataframe["service"] = resource["service"]
            dataframe["rating"] = rating
            dataframe["volume"] = float(resource["volume"])
            dataframe["extra"] = {
                k: v
                for k, v in resource["desc"].items()
                if not (k == "id" or k.endswith("_id"))
            }

            yield dataframe



cloud  = openstack_api.cloud_connection("Infomaniak")
data = project_dataframes(cloud, "cf35aa358c6e48c0b2fa2da14cdf91e4", "2022-02-13T06:00:00", "2022-02-14T06:00:00")
print (list(data))
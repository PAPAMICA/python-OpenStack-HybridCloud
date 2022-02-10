import openstack_api
cloud = openstack_api.cloud_connection('Infomaniak')
openstack_api.create_instance(cloud, "test_instance","Ubuntu 20.04 LTS Focal Fossa", "a1-ram2-disk20-perf1", "k8s-network", "keypair_test", "k8s-masters")
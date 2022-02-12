import subprocess
import os

def get_billing():

    
    file = "../plex-public-cloud/openrc"
    #file = f'/openrc/{cloud_name}'
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            line=line.split()
            if len(line) > 1:
                word=line[1].split('=')
                globals()[word[0]] = word[1]
    os.putenv('OS_AUTH_URL', OS_AUTH_URL)
    os.putenv('OS_PROJECT_NAME', OS_PROJECT_NAME)  
    os.putenv('OS_USERNAME', OS_USERNAME)
    os.putenv('OS_PASSWORD', OS_PASSWORD)  
    os.putenv('OS_REGION_NAME', OS_REGION_NAME)   
    os.putenv('OS_PROJECT_DOMAIN_NAME', OS_PROJECT_DOMAIN_NAME)  
    os.putenv('OS_USER_DOMAIN_NAME', OS_USER_DOMAIN_NAME)  
    lastmonth = ['m-1', '-b $(date -d "`date +%Y%m01` -1 month" +%Y-%m-%d) -e $(date -d "`date +%Y%m01` -1 day" +%Y-%m-%d)']
    thismonth = ['m', '-b $(date -d "`date +%Y%m01`" +%Y-%m-%d) -e $(date -d "`date +%Y%m01` +1 month -1 day" +%Y-%m-%d)']
    lastday = ['d-1', '-b $(date -d "`date +%Y-%m-%d` -1 day" +%Y-%m-%d) -e $(date -d "`date +%Y-%m-%d`" +%Y-%m-%d)']
    thisday = ['d', '-b $(date -d "`date +%Y-%m-%d`" +%Y-%m-%d)']
    delay = [lastmonth, thismonth, lastday, thisday]
    result = dict()
    for d in delay:
        data = subprocess.getoutput(f'openstack rating dataframes get {d[1]} -c Resources -f json | jq \'map(.Resources[].rating | tonumber) | add | . / 50\' ')
        data = round(float(data),2)
        result[d[0]] = data
    return result

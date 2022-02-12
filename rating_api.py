import subprocess

def get_billing(cloud_name):
    source = subprocess.getoutput(f'. /openrc/{cloud_name}')
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

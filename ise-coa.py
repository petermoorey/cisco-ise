import requests, sys, yaml
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# get the MnT node and MAC address of endpoint to reauthenticate
iseServer = sys.argv[1]
mac = sys.argv[2]

# lets define the PSNs that could be used to issue the COA
psns = ['mypsn01, 'mypsn02', 'mypsn03']

# get the MNT API username and password from a credentials file
creds = yaml.load(open('./secrets.yml'))
username = creds['ise-api']['username']
password = creds['ise-api']['password']

# define parameters for ISE connection
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ise = requests.session()
ise.auth = (username, password)
ise.verify = False
ise.disable_warnings = False
ise.timeout = 5
isePort = '443'

if __name__ == '__main__':
        # try each PSN until we get a success. Usually first PSN will work fine, but let's try each one until it is successful.
        for psn in psns:

                # the api call to trigger reauthentication
                url = 'https://{0}:{1}/admin/API/mnt/CoA/Reauth/{2}/{3}/1'.format(iseServer,isePort,psn,mac)

                # issue the api call
                result = ise.get(url, auth=HTTPBasicAuth(username, password), verify=False)

                # stop if ISE successfully issues the CoA
                if 'true' in result.text:
                        break

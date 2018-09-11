# <*******************
#
# Copyright 2018 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# *******************>
#AUTHOR: Akshay Karanth, SE, Juniper Networks
#!/usr/bin/python

DOCUMENTATION = '''
---
module: autodetectpermanagedhost
short_description: Enable/disable autodetection of log source for event collector
'''
EXAMPLES = '''
  tasks:
    - name: enable/disable autodetection of log source for event collector
      juniper_jsa_autodetectpermanagedhost:
        consoleip: "xx.xx.xx.xx"
        console_user: "admin"
        console_password: "password"
        component_id: "135"
        AUTODETECTION_ENABLED: "false"
      register: result

    - name: debug
      debug:
        var: result
'''

from ansible.module_utils.basic import *
import requests
import json
from requests.auth import HTTPBasicAuth

def autodetectpermanagedhost(data):


###
        url = "https://" + data['consoleip'] + "/api/config/deployment/hosts"
        urlparams= { "filter": "hostname=" + "\""+data['component_id'] + "\""}

        headers = {
            'Version': "9.0",
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Allow-Hidden': "true",
            'SEC': data['token']
            }
        response = requests.request("GET", url, auth = HTTPBasicAuth(data['console_user'], data['console_password']), verify = False, headers = headers, params = urlparams)
        try:
           if response.status_code == 200:
                a = response.json()
                host_id = response.json()[0]['id']
         #print(response.json())
         #print(response.json('id'))
           else:
                return True, False, {'response':response.json(), 'error': 'check component_id'}
        except IndexError:
           return True, False, {'response': response.json(), 'error': 'check component_id'}
###

###
        url = "https://" + data['consoleip'] + "/api/config/deployment/components"
        urlparams= { "filter": "host_id=" + "\""+ host_id.__str__() + "\"" + " and " + "type=" + "eventcollector" }

        response = requests.request("GET", url, auth = HTTPBasicAuth(data['console_user'], data['console_password']), verify = False, headers = headers, params = urlparams)
        try:
           if response.status_code == 200:
                a = response.json()
                actual_component_id = response.json()[0]['id']
         #print(response.json())
         #print(response.json('id'))
           else:
                return True, False, {'response':response.json(), 'error': 'make sure the host you gave has event collector component in it'}
        except IndexError:
           return True, False, {'response': response.json(), 'error': 'make sure the host you gave has event collector component in it'}
###


        #url = "https://xx.xx.xx.xx/api/config/access/users"
        url = "https://" + data['consoleip'] + "/api/config/deployment/staged_components/" + actual_component_id.__str__()

	querystring = {'updated_properties':
	    json.dumps(
		{
		"AUTODETECTION_ENABLED": data["AUTODETECTION_ENABLED"]
		})
	}


	response = requests.request("POST", url, auth = HTTPBasicAuth(data['console_user'], data['console_password']), verify = False, headers = headers, params = querystring)
#	print(response.text)
#	print(reponse.url)
#	print response.json()
#	return response.json()
	if response.status_code == 200:
		return False, True, response.json()

	return True, False, response.json()

def main():

    fields = {
        "consoleip": {"required": True, "type": "str"},
        "component_id": {"required": True, "type": "str"},
        "AUTODETECTION_ENABLED": {"required": True, "type": "str"},
	"console_user": { "type": "str"},
	"console_password": { "type": "str", "no_log": True},
	"token": { "type": "str", "no_log": True}
    }
    module = AnsibleModule(argument_spec=fields, required_one_of = [ ['console_password', 'token' ] ],mutually_exclusive = [ ['console_password', 'token' ] ], required_together =[['console_user', 'console_password']])
    is_error, has_changed, result = autodetectpermanagedhost (module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

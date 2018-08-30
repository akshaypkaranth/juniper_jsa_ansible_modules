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
      autodetectpermanagedhost:
        consoleip: "xx.xx.xx.xx"
        console_admin_password: "password"
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
            }
        response = requests.request("GET", url, auth = HTTPBasicAuth('admin', data['console_admin_password']), verify = False, headers = headers, params = urlparams)
        try:
           if response.status_code == 200:
                a = response.json()
                host_id = response.json()[0]['id']
         #print(response.json())
         #print(response.json('id'))
           else:
                return True, True, {'response':response.json(), 'error': 'check component_id'}
        except IndexError:
           return True, True, {'response': response.json(), 'error': 'check component_id'}
###

###
        url = "https://" + data['consoleip'] + "/api/config/deployment/components"
        urlparams= { "filter": "host_id=" + "\""+ host_id.__str__() + "\"" + " and " + "type=" + "eventcollector" }

        headers = {
            'Version': "9.0",
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Allow-Hidden': "true",
            }
        response = requests.request("GET", url, auth = HTTPBasicAuth('admin', data['console_admin_password']), verify = False, headers = headers, params = urlparams)
        try:
           if response.status_code == 200:
                a = response.json()
                actual_component_id = response.json()[0]['id']
         #print(response.json())
         #print(response.json('id'))
           else:
                return True, True, {'response':response.json(), 'error': 'make sure the host you gave has event collector component in it'}
        except IndexError:
           return True, True, {'response': response.json(), 'error': 'make sure the host you gave has event collector component in it'}
###


        #url = "https://xx.xx.xx.xx/api/config/access/users"
        url = "https://" + data['consoleip'] + "/api/config/deployment/staged_components/" + actual_component_id.__str__()

	querystring = {'updated_properties':
	    json.dumps(
		{
		"AUTODETECTION_ENABLED": data["AUTODETECTION_ENABLED"]
		})
	}


	headers = {
	    'Version': "9.0",
	    'Accept': "application/json",
	    'Content-Type': "application/json",
	    'Allow-Hidden': "true",
	    #'Authorization': "Basic YWRtaW46am5wcjEyMyE=",
	    #'Cache-Control': "no-cache",
	    #'Postman-Token': "342af374-ad5a-4846-a7ee-398e3cf6ed63"
	    }

	response = requests.request("POST", url, auth = HTTPBasicAuth('admin', data['console_admin_password']), verify = False, headers = headers, params = querystring)
#	print(response.text)
#	print(reponse.url)
#	print response.json()
#	return response.json()
	if response.status_code == 200:
		return False, True, response.json()

	return True, True, response.json()

def main():

    fields = {
        "consoleip": {"required": True, "type": "str"},
        "console_admin_password": {"required": True, "type": "str", "no_log": True},
        "component_id": {"required": True, "type": "str"},
        "AUTODETECTION_ENABLED": {"required": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = autodetectpermanagedhost (module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

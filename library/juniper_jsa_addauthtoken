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
module: adduser
short_description: Add new user to JSA
'''
EXAMPLES = '''
  tasks:
    - name: add new user to JSA
      adduser:
        consoleip: "xx.xx.xx.xx"
        console_admin_password: "password"
        description: "test user 51"
        email: "user51@juniper.net"
        password: "Password123!"
        role_id: 2
        security_profile_id: 1
        username: "user56"
      register: result

    - name: debug
      debug:
        var: result
'''

from ansible.module_utils.basic import *
import requests
import json
from requests.auth import HTTPBasicAuth

def addauthtoken(data):

        #url = "https://xx.xx.xx.xx/api/config/access/users"
        url = "https://" + data['consoleip'] + "/api/config/access/staged_authorized_services"

	querystring = {
		'name': data['name'],
		'security_profile_id': data['security_profile_id'],
		'role_id': data['role_id']
		}


	headers = {
	    'Version': "9.0",
	    'Accept': "application/json",
	    'Content-Type': "application/json",
	    'Allow-Hidden': "true"
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
        "role_id": {"default": True, "type": "int"},
        "security_profile_id": {"default": True, "type": "int"},
        "name": {"required": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = addauthtoken(module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

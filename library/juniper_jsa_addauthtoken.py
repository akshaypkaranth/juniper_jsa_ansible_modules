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
module: juniper_jsa_addauthtoken
short_description: Add auth token
'''
EXAMPLES = '''
  tasks:
    - name: add authentication token to JSA
      juniper_jsa_addauthtoken:
        consoleip: "xx.xx.xx.xx"
        console_password: "password"
        console_user: "admin"
        role_id: 2
        security_profile_id: 1
        name: "testfromansible"

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
	    'Allow-Hidden': "true",
            'SEC': data['token']
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
        "role_id": {"default": True, "type": "int"},
        "security_profile_id": {"default": True, "type": "int"},
        "name": {"required": True, "type": "str"},
	"console_user": { "type": "str"},
	"console_password": { "type": "str", "no_log": True},
	"token": { "type": "str", "no_log": True}
 }
    module = AnsibleModule(argument_spec=fields, required_one_of = [ ['console_password', 'token' ] ],mutually_exclusive = [ ['console_password', 'token' ] ], required_together =[['console_user', 'console_password']])
    is_error, has_changed, result = addauthtoken(module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

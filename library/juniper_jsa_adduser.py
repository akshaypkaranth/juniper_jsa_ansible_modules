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
        console_admin_password: "password!"
        description: "test user 51"
        email: "user51@juniper.net"
        password: "Password123!"
        role_id: "Admin"
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

def postUsers(data):
###
	url = "https://" + data['consoleip'] + "/api/config/access/staged_roles"
	urlparams= { "filter": "name=" + data['role_id']}
        headers = {
            'Version': "9.0",
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Allow-Hidden': "true",
            'SEC': data['token']
}
	try:
		response = requests.request("GET", url, auth = HTTPBasicAuth(data['console_user'], data['console_password']), verify = False, headers = headers, params = urlparams)
	#actual_role_id = response.json()[0]['id']
                #return True, False, response.json()
	#f1 = open('/root/jsa-modules/file.txt','w+')
	#f1.write('debug log')
	except exception as e:
		return True, False, {'python exception': str(e)}		
        #return False, False, { 'msg' : response.status_code, 'size': len(response.json()) }
        if response.status_code == 200 and (len(response.json()) > 0):
                actual_role_id = response.json()[0]['id']
	elif response.status_code == 200 and (len(response.json()) == 0):
		return True, False, { 'msg': 'role id you entered does not exist' }
	else:
		return True, False, response.json()


###

        #url = "https://xx.xx.xx.xx/api/config/access/users"
        url = "https://" + data['consoleip'] + "/api/config/access/users"

	querystring = {'user':
	    json.dumps(
		{
		'consoleip': data['consoleip'],
		'description': data['description'],
		'email': data['email'],
		'password': data['password'],
		'role_id': actual_role_id,
		'security_profile_id': data['security_profile_id'],
		'username': data['username']
		})
	}


	headers = {
	    'Version': "9.0",
	    'Accept': "text/plain",
	    'Content-Type': "application/json",
	    'Allow-Hidden': "true",
            'SEC': data['token']
	    #'Authorization': "Basic YWRtaW46am5wcjEyMyE=",
	    #'Cache-Control': "no-cache",
	    #'Postman-Token': "342af374-ad5a-4846-a7ee-398e3cf6ed63"
	    }

	try:
		response = requests.request("POST", url, auth = HTTPBasicAuth(data['console_user'], data['console_password']), verify = False, headers = headers, params = querystring)

	except Exception as e:
		return True, False, {'python exception': str(e)}
	#return False, True, response.json()


	if response.status_code == 200:
		return False, True, { 'msg': 'user add success - api endpoint returns empty body' }
	elif response.status_code == 422:
                return False, False, response.json()
	return True, False, response.json()

def main():

    fields = {
        "consoleip": {"required": True, "type": "str"},
        "description": {"required": True, "type": "str"},
        "email": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str", "no_log": True},
        "role_id": {"default": True, "type": "str"},
        "security_profile_id": {"default": True, "type": "int"},
        "username": {"required": True, "type": "str"},
        "console_user": { "type": "str"},
	"console_password": { "type": "str", "no_log": True},
	"token": { "type": "str", "no_log": True}
    }
    module = AnsibleModule(argument_spec=fields, required_one_of = [ ['console_password', 'token' ] ],mutually_exclusive = [ ['console_password', 'token' ] ], required_together =[['console_user', 'console_password']])
    is_error, has_changed, result = postUsers (module.params)
    #import pdb
    #pdb.set_trace()
#    is_error, has_changed, result = 0, 0, postUsers(fields)

    #module.exit_json(changed=has_changed, meta=result)
    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg='error', meta=result)
'''
    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg='failed', meta=result)
'''

if __name__ == '__main__':
    main()

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
module: getusers
short_description: Get all the users currently staged in JSA
'''
EXAMPLES = '''
    - name: get users
      getusers:
         description: "get all users"
         consoleip: "xx.xx.xx.xx"
         console_admin_password: "password"
      register: result

    - name: debug
      debug:
        var: result
'''

from ansible.module_utils.basic import *
import requests
import json
from requests.auth import HTTPBasicAuth

def getusers(data):

	url = "https://" + data['consoleip']+ "/api/config/access/users"

	querystring = {'user':
	    json.dumps(
		{
		'description': data['description'],
		})
	}


	headers = {
	    'Version': "9.0",
	    #'Accept': "text/plain",
	    'Content-Type': "application/json",
	    'Allow-Hidden': "true",
            'SEC': data['token']
	    #'Authorization': "Basic YWRtaW46am5wcjEyMyE=",
	    #'Cache-Control': "no-cache",
	    #'Postman-Token': "342af374-ad5a-4846-a7ee-398e3cf6ed63"
	    }

	response = requests.request("GET", url, auth = HTTPBasicAuth(data['console_user'], data['console_password']), verify = False, headers = headers)
#	print(response.text)
#	print(reponse.url)
#	print response.json()
#	return response.json()
	if response.status_code == 200:
		return False, True, response.json()

	return True, True, response.json()

def main():

    fields = {
 "description": {"required": True, "type": "str"},
"consoleip": {"required": True, "type": "str"},
"console_user": { "type": "str"},
"console_password": { "type": "str", "no_log": True},
"token": { "type": "str", "no_log": True}
}
    module = AnsibleModule(argument_spec=fields, required_one_of = [ ['console_password', 'token' ] ],mutually_exclusive = [ ['console_password', 'token' ] ], required_together =[['console_user', 'console_password']])
    is_error, has_changed, result = getusers (module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

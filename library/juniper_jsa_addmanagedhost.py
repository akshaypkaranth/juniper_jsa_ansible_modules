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
module: addmanagedhost
short_description: Add a managed host to JSA
'''
EXAMPLES = '''
  tasks:
    - name: add a managed host
      juniper_jsa_addmanagedhost:
         consoleip: "xx.xx.xx.xx"
         token: "2e92ea54-f196-4008-bf1a-2a2a63eab4b8"
         managed_host_ip: "xx.xx.xx.xx"
         managed_host_password: "password"
      register: result

    - name: debug
      debug:
        var: result
'''

from ansible.module_utils.basic import *
import requests
import json
from requests.auth import HTTPBasicAuth

def addmanagedhost(data):

        #url = "https://xx.xx.xx.xx/api/config/access/users"
        url = "https://" + data['consoleip'] + "/api/config/deployment/staged_hosts"

        querystring = {
    #"compressed": true,
    #"encrypted": true,
    "ip": data['managed_host_ip'],
    "password": data['managed_host_password']
}

        headers = {
	    'Version': "9.0",
	    'Accept': "application/json",
	    'Content-Type': "application/json",
	    'Allow-Hidden': "true",
            'SEC': data['token']
	    }

        response = requests.request("POST", url, auth = HTTPBasicAuth(data['console_user'], data['console_password']), verify = False, headers = headers, data = json.dumps(querystring))
#	print(response.texton
#	print(reponse.url)
#	print response.json()
#	return response.json()
	if response.status_code < 300:
		return False, True, response.json()
	if response.status_code == 422:
		return False, False, response.json()
        return True, False, response.json()


def main():

    fields = {
        "consoleip": {"required": True, "type": "str"},
        "managed_host_ip": {"required": True, "type": "str"},
        "managed_host_password": {"required": True, "type": "str", "no_log": True},
        "console_user": { "type": "str"},
	"console_password": { "type": "str", "no_log": True},
	"token": { "type": "str", "no_log": True}
    }
    module = AnsibleModule(argument_spec=fields, required_one_of = [ ['console_password', 'token' ] ],mutually_exclusive = [ ['console_password', 'token' ] ], required_together =[['console_user', 'console_password']])
    is_error, has_changed, result= addmanagedhost(module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

#    is_error, has_changed, result, debug = deploy()

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

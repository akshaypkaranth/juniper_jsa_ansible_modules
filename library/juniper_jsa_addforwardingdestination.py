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
module: add_forwarding_destination
short_description: add new forwarding destination
'''
EXAMPLES = '''
  tasks:
    - name: add new forwarding destination
      juniper_jsa_addforwardingdestination:
        consoleip: "xx.xx.xx.xx"
	console_user: "admin"
        console_password: "password!"
        event_format: "JSON"
        forwarding_ip: "30.30.30.30"
        name: "mytest"
        port: 53
        protocol: "TCP"
      register: result

    - name: debug
      debug:
        var: result
'''

from ansible.module_utils.basic import *
import requests
import json
from requests.auth import HTTPBasicAuth


def add_forwarding_destination(data):

        #url = "https://xx.xx.xx.xx/api/config/access/users"
        url = "https://" + data['consoleip'] + "/api/config/selective_forwarding/destinations"
#	bool true= True
        querystring = {
"create_missing_header": bool(1),
"enabled": bool(1),
"event_format": data['event_format'],
"ip_address": data['forwarding_ip'],
"name": data['name'],
"port": data['port'],
"protocol": data['protocol']
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
	if response.status_code == 201:
		#deploy()
		return False, True, response.json()
        return True, True, response.json()


def main():

    fields = {
        "consoleip": {"required": True, "type": "str"},
        "event_format": {"required": True, "type": "str"},
        "forwarding_ip": {"required": True, "type": "str"},
	"name": {"required": True, "type": "str"},
        "port": {"required": True, "type": "int"},
        "protocol": {"required": True, "type": "str"},
	"console_user": { "type": "str"},
	"console_password": { "type": "str", "no_log": True},
	"token": { "type": "str", "no_log": True}
    }
    module = AnsibleModule(argument_spec=fields, required_one_of = [ ['console_password', 'token' ] ],mutually_exclusive = [ ['console_password', 'token' ] ], required_together =[['console_user', 'console_password']])
    is_error, has_changed, result= add_forwarding_destination (module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

#    is_error, has_changed, result, debug = deploy()

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

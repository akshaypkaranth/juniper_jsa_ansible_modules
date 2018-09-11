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
module: add_routing_rule
short_description: Add new routing rule to JSA
'''
EXAMPLES = '''
  tasks:
    - name: add routing rule
      add_routing_rule:
        consoleip: "xx.xx.xx.xx"
        console_admin_password: "password"
        component: 103
        database: "events"
        description: "test via api"
        destination: 3
        mode: "online"
        name: "routing_rule_via_ansible"
        routing_option: "FORWARD_AND_CORRELATE"
      register: result
'''

from ansible.module_utils.basic import *
import requests
import json
from requests.auth import HTTPBasicAuth


def add_routing_rule(data):

###
        url = "https://" + data['consoleip'] + "/api/config/event_sources/event_collectors"
        logsrc = "Juniper Junos OS Platform"
        urlparams= { "filter": "name=" + "\""+data['component'] + "\""}

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
            actual_component = response.json()[0]['id']
          else:
            return True, False, {'error': 'check target event collector id'}
        except IndexError:
                return True, False, {'error': 'check target event collector id'}

###

###
        url = "https://" + data['consoleip'] + "/api/config/selective_forwarding/destinations"
        logsrc = "Juniper Junos OS Platform"
        urlparams= { "filter": "name=" + "\""+data['destination'] + "\""}

        response = requests.request("GET", url, auth = HTTPBasicAuth(data['console_user'], data['console_password']), verify = False, headers = headers, params = urlparams)
        try:
          if response.status_code == 200:
            actual_destination = response.json()[0]['id']
          else:
            return True, False, {'response': response.json(), 'error': 'check target event collector id'}
        except IndexError:
                return True, False, {'response': response.json(), 'error': 'check target event collector id'}

###


        #url = "https://xx.xx.xx.xx/api/config/access/users"
        url = "https://" + data['consoleip'] + "/api/config/selective_forwarding/routes"
#	bool true= True
        querystring = {
"component": actual_component,
"database": data['database'],
"description": data['description'],
"destinations": [actual_destination],
"enabled": bool(1),
"match_all": bool(1),
"mode": data['mode'],
"name": data['name'],
"routing_option": data['routing_option']
}


        response = requests.request("POST", url, auth = HTTPBasicAuth(data['console_user'], data['console_password']), verify = False, headers = headers, data = json.dumps(querystring))
#	print(response.texton
#	print(reponse.url)
#	print response.json()
#	return response.json()
	if response.status_code == 201:
		#deploy()
		return False, True, response.json()
        return True, False, response.json()


def main():

    fields = {
        "consoleip": {"required": True, "type": "str"},
        "component": {"required": True, "type": "str"},
        "database": {"required": True, "type": "str"},
	"description": {"required": True, "type": "str"},
        "destination": {"required": True, "type": "str"},
        "mode": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "routing_option": {"required": True, "type": "str"},
	"console_user": { "type": "str"},
	"console_password": { "type": "str", "no_log": True},
	"token": { "type": "str", "no_log": True}
    }
    module = AnsibleModule(argument_spec=fields, required_one_of = [ ['console_password', 'token' ] ],mutually_exclusive = [ ['console_password', 'token' ] ], required_together =[['console_user', 'console_password']])
    is_error, has_changed, result = add_routing_rule(module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

#    is_error, has_changed, result, debug = deploy()

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

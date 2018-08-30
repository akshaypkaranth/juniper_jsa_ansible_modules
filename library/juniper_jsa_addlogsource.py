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
module: addlogsource
short_description: add new log source to JSA
'''
EXAMPLES = '''
  tasks:
    - name: add new log source to JSA
      addlogsource:
         name: "mytest"
         description: "log source added from ansible"
         consoleip: "xx.xx.xx.xx"
         console_admin_password: "password"
         log_source_identifier: "myvsrx"
         credibility: 5
         target_event_collector_id: 103
         log_source_type_id: 64
      register: result

    - name: debug
      debug:
        var: result
'''

from ansible.module_utils.basic import *
import requests
import json
from requests.auth import HTTPBasicAuth

def addlogsource(data):

###
        url = "https://" + data['consoleip'] + "/api/config/event_sources/log_source_management/log_source_types"
        urlparams= { "filter": "name=" + "\""+data['log_source_type_id'] + "\""}

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
           	actual_log_source_type_id = response.json()[0]['id']
         #print(response.json())
         #print(response.json('id'))
           else:
           	return True, True, {'response':response.json(), 'error': 'check log source type'}
        except IndexError:
	   return True, True, {'response': response.json(), 'error': 'check log source type'}  
###

###
	url = "https://" + data['consoleip'] + "/api/config/event_sources/event_collectors"
	logsrc = "Juniper Junos OS Platform"
        urlparams= { "filter": "name=" + "\""+data['target_event_collector_id'] + "\""}

        headers = {
            'Version': "9.0",
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Allow-Hidden': "true",
            }
        response = requests.request("GET", url, auth = HTTPBasicAuth('admin', "Juniper321!"), verify = False, headers = headers, params = urlparams)
        try:
          if response.status_code == 200:
            actual_target_event_collector_id = response.json()[0]['id']
          else:
            return True, True, {'response': response.json(), 'error': 'check target event collector id'}
        except IndexError:
		return True, True, {'response': response.json(), 'error': 'check target event collector id'}
         
###
        #url = "https://xx.xx.xx.xx/api/config/access/users"
        url = "https://" + data['consoleip'] + "/api/config/event_sources/log_source_management/log_sources"

        querystring = {
    'protocol_parameters': [{
        'name': 'identifier',
        'value': data['log_source_identifier']
    }, {
        'name': 'incomingPayloadEncoding',
        'value': 'UTF-8'
    }],
    'description': 'efgh',
    'name': data['name'],
    'type_id': actual_log_source_type_id,
    #'coalesce_events': true,
    'credibility': data['credibility'],
    #'store_event_payload': true,
    'target_event_collector_id': actual_target_event_collector_id,
    #'enabled': true,
    'protocol_type_id': 0
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

        response = requests.request("POST", url, auth = HTTPBasicAuth('admin', data['console_admin_password']), verify = False, headers = headers, data = json.dumps(querystring))
#	print(response.texton
#	print(reponse.url)
#	print response.json()
#	return response.json()
	if response.status_code == 200|201:
		#deploy()
		return False, True, response.json()
        return True, True, response.json()


def main():

    fields = {
        "consoleip": {"required": True, "type": "str"},
        "console_admin_password": {"required": True, "type": "str", "no_log": True},
        "description": {"required": True, "type": "str"},
        "log_source_identifier": {"required": True, "type": "str"},
	"credibility": {"required": True, "type": "int"},
        "target_event_collector_id": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "log_source_type_id": {"required": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result= addlogsource (module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

#    is_error, has_changed, result, debug = deploy()

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

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
module: overwrite_network_hierarchy
short_description: Overwrite network hierarchy in JSA
'''
EXAMPLES = '''
  tasks:
    - name: overwriting network hierarchy
      overwrite_network_hierarchy:
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


def overwrite_network_hierarchy(data):

        #url = "https://xx.xx.xx.xx/api/config/access/users"
        url = "https://" + data['consoleip'] + "/api/config/network_hierarchy/staged_networks"
#	bool true= True
	with open('/root/jsa-modules/library/input.json') as f:
    		parsedinput = json.load(f)
        querystring = parsedinput["input"]


        headers = {
	    'Version': "9.0",
	    'Accept': "application/json",
	    'Content-Type': "application/json",
	    'Allow-Hidden': "true",
	    #'Authorization': "Basic YWRtaW46am5wcjEyMyE=",
	    #'Cache-Control': "no-cache",
	    #'Postman-Token': "342af374-ad5a-4846-a7ee-398e3cf6ed63"
	    }

        response = requests.request("PUT", url, auth = HTTPBasicAuth('admin', data['console_admin_password']), verify = False, headers = headers, data = json.dumps(querystring))
#	print(response.texton
#	print(reponse.url)
#	print response.json()
#	return response.json()
	if response.status_code == 200:
		return False, True, response.json()
		#deploy()
		#return False, True, {"message": "Success ! Network Hierarchy replaced by new value !"}, {"message2": "all good"}
        return True, True, response.json()


def main():

    fields = {
        "consoleip": {"required": True, "type": "str"},
	"console_admin_password": {"required": True, "type": "str", "no_log": True}
        #"input": {"required": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = overwrite_network_hierarchy(module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

#    is_error, has_changed, result, debug = deploy()

    if not is_error:
        module.exit_json(changed=has_changed, meta=debug)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()

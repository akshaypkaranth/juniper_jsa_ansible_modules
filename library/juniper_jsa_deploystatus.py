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
module: deploy
short_description: INCREMENTAL or FULL deploy changes to JSA
'''
EXAMPLES = '''
  tasks:
    - name: INCREMENTAL or FULL deploy changes to JSA
      deploy:
         consoleip: "xx.xx.xx.xx"
         console_admin_password: "password!"
         type: "INCREMENTAL"
      register: result

    - name: debug
      debug:
        var: result
'''

from ansible.module_utils.basic import *
import requests
import json
from requests.auth import HTTPBasicAuth

def deploy(data):

        url = "https://" + data['consoleip'] + "/api/staged_config/deploy_status"
        #querystring = { "type": data['type'] }
        headers = {
            'Version': "9.0",
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Allow-Hidden': "true",
            #'Authorization': "Basic YWRtaW46am5wcjEyMyE=",
            #'Cache-Control': "no-cache",
            #'Postman-Token': "342af374-ad5a-4846-a7ee-398e3cf6ed63"
            }
        response = requests.request("GET", url, auth = HTTPBasicAuth('admin', data['console_admin_password']), verify = False, headers = headers)

        if response.status_code < 300:
                return False, True, response.json()
        return True, True, response.json()
        #return

def main():

    fields = {
        "consoleip": {"required": True, "type": "str"},
        "console_admin_password": {"required": True, "type": "str", "no_log": True},
        #"type": {"required": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = deploy (module.params)
#    is_error, has_changed, result = 0, 0, postUsers(fields)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed", meta=result)


if __name__ == '__main__':
    main()


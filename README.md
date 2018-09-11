# juniper_jsa_ansible_modules
Custom Ansible Modules for Juniper Secure Analytics (JSA) aka QRADAR
## update

All modules now support 'console_user' and 'console_password' for Basic Authentication

OR

'token' for SEC authentication 

## How to use these Ansible modules:
Step 1 : Clone this repo.
Step 2: Edit the example playbooks (.yml files) as per your environment.
Step 3: Run: ansible-playbook file.yml -vvv
## Examples:

    - name: add authentication token to JSA
      juniper_jsa_addauthtoken:
        consoleip: "xx.xx.xx.xx"
	console_user: "admin"
        console_password: "password!"
        role_id: 2
        security_profile_id: 1
        name: "testfromansible"
all above parameters are self explanatory.

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
	
1.event_format can be PAYLOAD or NORMALIZED or JSON
2.protocol can be  TCP or UDP or SSL


    - name: add new log source to JSA
      juniper_jsa_addlogsource:
         name: "mytestnew2"
         description: "new 2 log source added from ansible"
         consoleip: "xx.xx.xx.xx"
         console_user: "admin"
         console_password: "password!"
         log_source_identifier: "myvsrxnew2"
         credibility: 5
         target_event_collector_id: "eventcollector103 :: JSA731p4eventproc"
         log_source_type_id: "Juniper Junos OS Platform"

all above parameters are self explanatory.


    - name: add a managed host
      juniper_jsa_addmanagedhost:
         consoleip: "xx.xx.xx.xx"
         console_user: "admin"
         console_password: "password!"
         managed_host_ip: "xx.xx.xx.xx"
         managed_host_password: "password!"

all above parameters are self explanatory.

    - name: add routing rule
      juniper_jsa_addroutingrule:
        consoleip: "xx.xx.xx.xx"
        console_user: "admin"        
	console_password: "password!"
        component: "eventcollector103 :: JSA731p4eventproc"
        database: "events"
        description: "test via api3"
        destination: "mytest"
        mode: "online"
        name: "routing_rule_via_ansible4"
        routing_option: "FORWARD_AND_CORRELATE"
1.database can be events or flows
2.mode can be online or offline
3.routing_option can be one of  FORWARD_AND_CORRELATE, FORWARD_NO_CORRELATE, FORWARD_AND_DROP, CORRELATE, NO_CORRELATE, DROP






    - name: add new user to JSA
      juniper_jsa_adduser:
        consoleip: "xx.xx.xx.xx"
        console_user: "admin"
        console_password: "password!"
        description: "test user 555"
        email: "user51@juniper.net"
        password: "Password123!"
        role_id: "All"
        security_profile_id: 1
        username: "user1234567"
	

all above parameters are self explanatory.

    - name: enable/disable autodetection of log source for event collector
      juniper_jsa_autodetectpermanagedhost:
        consoleip: "xx.xx.xx.xx"
        console_user: "admin"
        console_password: "password!"
        component_id: "JSA731p4console"
        AUTODETECTION_ENABLED: "false"
      register: result
      
      
 all above parameters are self explanatory. 
 
  
    - name: INCREMENTAL or FULL deploy changes to JSA
      juniper_jsa_deploy:
         consoleip: "xx.xx.xx.xx"
         console_user: "admin"
         console_password: "password!"
         type: "INCREMENTAL"

1.type  can be "INCREMENTAL" or "FULL"





    - name: get current deployment nodes
      juniper_jsa_getcurrentdeployment:
         consoleip: "xx.xx.xx.xx"
         console_user: "admin"
         console_password: "password!"
	 

all above parameters are self explanatory.

    - name: get all users staged in JSA
      juniper_jsa_getusers:
         description: "get all users"
         consoleip: "xx.xx.xx.xx"
         console_user: "admin"
         console_password: "password!"
	 

all above parameters are self explanatory.


    - name: overwriting network hierarchy
      juniper_jsa_overwritenetworkhierarchy:
         consoleip: "xx.xx.xx.xx"
         console_user: "admin"
         console_password: "password!"
		 
all above parameters are self explanatory.

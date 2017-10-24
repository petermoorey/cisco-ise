# Cisco ISE Scripts

Various scripts relating to Cisco ISE automation and APIs

## ISE Change of Authorization (CoA) - ise-coa.py

Script used to trigger a Change of Authorization (CoA), reauthenticating an endpoint.  The script is called using the command below, insert the FQDN of the ISE MNT node, and endpoint MAC address to be reauthenticated:

 ```python ise-coa.py mnt.ise.company.com 11:22:33:44:55:66```

## ISE Switch Config Generator - ise-generate-switch-config.py
Script used to generate the additional configuration required to enable Cisco ISE on a LAN switch.  The script parses a given switch configuration file and creates a new file containing the global and interface-level commands required to enable ISE.  The script is called using the command below, replace the file name with a file containing the current switch config.

 ```python ise-generate-switch-config sample-switch-config.txt```
 
 Example of output after running script:
 
 ```--------------------
Issue the command below to apply configuration:
copy ftp://myuser:mypass@myserver.com/cfgs/switch.txt running-config
   NAC Exempt:  FastEthernet0/7 (Uplink to core switch)
   NAC Exempt:  FastEthernet0/9 (printer near office 122A)
   NAC Exempt:  FastEthernet0/24 (No Description)
--------------------```

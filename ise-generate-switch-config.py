import requests, os, re, sys
from ciscoconfparse import CiscoConfParse

# function to get switch config from file
def getConfig():
	configFile = sys.argv[1]
	with open(configFile, 'r') as configFile:
		configFile = configFile.read()
	return configFile


# function to write new configuration to file
def writeToFile(switch, config):
	filename = "./%s.txt" % (switch)
	with open(filename, "w") as f:
		f.write(config)
		f.close()

if __name__ == '__main__':

	# get current switch config
	configFile = getConfig()

	# load templates from files 
	iseGeneralConfig = './sample-ise-general-config.txt'
	iseInterfaceConfig = './sample-ise-interface-config.txt'
	with open(iseGeneralConfig, 'r') as iseGeneralConfig:
		iseGeneralConfig = iseGeneralConfig.read()
	with open(iseInterfaceConfig, 'r') as iseInterfaceConfig:
		iseInterfaceConfig = iseInterfaceConfig.read().splitlines() 

	# create list to contain new config commands
	new_config_cmds = []
	skipped_interfaces = []
	parse = CiscoConfParse(configFile.split("\n"))
	new_config_cmds.append(iseGeneralConfig)

	# find switch hostname
	device_name = parse.find_lines("^hostname\s")
	device_name = device_name[0].replace("hostname ", "")

	print "-" * 20
	print "Issue the command below to apply configuration:"
	print "copy ftp://myuser:mypass@myserver.com/cfgs/%s.txt running-config" % device_name.lower()

	# for each interface in config
	for intf in parse.find_objects(r'^interface.+?thernet'):
		
		# if the port is not exempt from NAC
		interface_not_exempt = not intf.has_child_with(r'(?i)mode trunk|^\s+channel|^\s+description.+(Server|Printer|Uplink)|^\s+shutdown')
		if interface_not_exempt:
		
			# add interface to new config commands 
			new_config_cmds.append(intf.text)

			# for each ISE interface command
			for command in iseInterfaceConfig:

				regex = "r\"^%s\"" % command
				has_cmd = intf.has_child_with(regex)

				# if an interface command is missing append it to the new config
				if not has_cmd:
					new_config_cmds.append(" %s" % command)
					
				for i in intf.children:
					regexPortSecurity = re.compile(r'port-security')

					# remove any port security commands
					if regexPortSecurity.search(i.text) is not None:
						redactedCmd = " no %s" % i.text.lstrip()
						new_config_cmds.append(redactedCmd)

			# include a shut/no shut to reset the port
			new_config_cmds.append(" shutdown")
			new_config_cmds.append(" no shutdown")
			new_config_cmds.append("!")
		
		else:
			# for each interface exempt from NAC
			desc = None

			# extract the interface description
			for i in intf.children:
				if 'description' in i.text:
					desc = i.text
					desc = desc.replace("description", "").strip()
			if desc is None:
				desc = "No Description"

			# print skipped interface names and descriptions 
			intfce = intf.text
			intfce = intfce.replace("interface","")
			print "   NAC Exempt: %s (%s)" % (intfce, desc)

	# end the config with 'end' so it is parsed correctly by switch
	new_config_cmds.append("end")
	# write all the new commands required to enable ISE to local file
	writeToFile(device_name, "\n".join(new_config_cmds))
	print "-" * 20


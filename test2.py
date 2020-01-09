from netmiko import ConnectHandler

cisco_881 = {
    'device_type': 'cisco_ios_telnet',
    'ip':   '192.168.136.130',
    'port' : '2002',
    'username': 'bvadmin',
    'password': 'Bv@dm1n',
}

def cisco_prompt_reset(connection):# :netmiko.BaseConnection):
	if connection.check_enable_mode():
		connection.exit_enable_mode()
	if connection.check_config_mode():
		connection.exit_config_mode()


net_connect= ConnectHandler(**cisco_881)
prompt=net_connect.find_prompt()
print(prompt)
cisco_prompt_reset(net_connect)
prompt=net_connect.find_prompt()
print(prompt)

op=net_connect.send_command("show ip int brief")
print(op)

#enable, config t, int xx, no shut, end, exit

eths=op.splitlines()
for eth in eths:
	ethprops=eth.split()
	#print (ethprops)
	#print(ethprops[0] + "- " + ethprops[5])
	if(ethprops[5] == 'down'):
		net_connect.enable();
		net_connect.config_mode()
		net_connect.send_config_set(['int ' + ethprops[0], 'no shut'])
		net_connect.exit_config_mode()
		net_connect.exit_enable_mode()


print("final status check")
op=net_connect.send_command("show ip int brief")
print(op)
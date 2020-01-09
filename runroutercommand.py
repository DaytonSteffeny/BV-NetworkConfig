from netmiko import ConnectHandler
import netmiko
import paramiko
from netmiko import log
import logging


from paramiko import ProxyCommand

#logging.basiconfig(level=logging.DEBUG)

def cisco_prompt_reset(connection):# :netmiko.BaseConnection):
	if connection.check_enable_mode():
		connection.exit_enable_mode()
	if connection.check_config_mode():
		connection.exit_config_mode()

def connect_device(devicedetails, retry=True):
	net_connect = None
	try:
		net_connect = ConnectHandler(**devicedetails)
	except Exception as e:
		print(e)
		if(str(e).find("login failed") > -1):
			return connect_device(devicedetails, False)
	return net_connect

cisco_881 = {
	'device_type': 'cisco_ios_telnet',
	'ip': '192.168.136.130',
	'port': '2001'
	'username': 'bvadmin'
	'password': 'Bv@dmin'
#	'allow_agent':'False',
#	'use_keys':'False',
#	'look_for_keys':'False',
#	'global_delay_factor': 2,
}

print("Trying connection to device")
net_connect = connect_device(cisco_881)
if(net_connect == None):
	print("Could not connect to devicce. Not proceeding further.")
	exit()

cisco_prompt_reset(net_connect)
prompt=net_connect.find_prompt()
print(prompt)

print ('Running first status check')
cmdout=net_connect.send_command("show ip int brief")
print(cmdout)

eths=cmdout.splitlines()
for eth in eths:
	ethprops=eth.split()
	if(ethprops[5]=='down'):
		print(ethprops[0] + ' is down. bringing up')
		op = net_connect.enable()
		print(op)
		op = net_connect.config_mode()
		print(op)
		op = net_connect.send_config_set(["int " + ethprops[0], "no shut"])
		print(op)
		op = net_connect.exit_config_mode()
		print(op)
print ('Running final status check')
cmdout=net_connect.send_command("show ip int brief")
print(cmdout)


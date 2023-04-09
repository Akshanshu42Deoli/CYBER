#! /usr/bin/env python

import subprocess
import optparse
import re


# without using variable

# subprocess.call("ifconfig eth0 down",shell=True)
# subprocess.call("ifconfig eth0 hw ether 22:33:44:55:66:77",shell=True)
# subprocess.call("ifconfig eth0 up",shell=True)


# using variable

#
# interface = "eth0"
# new_mac = "00:44:66:88:99:55"
#
# print("[+] CHANGING MAC ADDRESS "+interface+"TO "+new_mac)
# subprocess.call("ifconfig " + interface + " down",shell=True)
# subprocess.call("ifconfig "+ interface + " hw ether "+new_mac,shell=True)
# subprocess.call("ifconfig "+interface+" up",shell=True)


# using input method

#
# interface = input("Enter the interface : ")
# new_mac = input("Enter the new mac address : ")
#
# print("[+] CHANGING MAC ADDRESS "+interface+" TO "+new_mac)
# subprocess.call("ifconfig " + interface + " down",shell=True)
# subprocess.call("ifconfig "+ interface + " hw ether "+new_mac,shell=True)
# subprocess.call("ifconfig "+interface+" up",shell=True)

# Handle user input


# interface = input("Enter the interface : ")
# new_mac = input("Enter the new mac address : ")
#
# print("[+] CHANGING MAC ADDRESS "+interface+" TO "+new_mac)
# subprocess.call(["ifconfig" , interface , "down"])
# subprocess.call(["ifconfig", interface , "hw","ether",new_mac])
# subprocess.call(["ifconfig",interface,"up"])

# command line arguments


def change_mac(interface, new_mac):
    print('[+] CHANGING MAC ADDRESS ' + str(interface) + " TO " + str(new_mac))
    subprocess.call(["ifconfig", str(interface), "down"])
    subprocess.call(["ifconfig", str(interface), "hw", "ether", str(new_mac)])
    subprocess.call(["ifconfig", str(interface), "up"])


def get_arg():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="mac", help="New mac address")
    (option, arg) = parser.parse_args()
    if not option.interface:
        parser.error("[+] Please specify the interface (-i) , --help for help")
    elif not option.mac:
        parser.error("[+] Please specify the mac (-m) , --help for help")
    return option


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    new_mac_ifconfig = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if new_mac_ifconfig:
        return new_mac_ifconfig.group(0)
    else:
        print("[+]cannot find mac address")


option = get_arg()
interface = option.interface
new_mac = option.mac
curr_mac = get_current_mac(interface)
print("[+]current mac : " + str(curr_mac))
change_mac(interface, new_mac)
curr_mac = get_current_mac(interface)
if (curr_mac == new_mac):
    print("[+] The mac address is successfully changed to " + new_mac)
else:
    print("[+] Mac address did not changed ")

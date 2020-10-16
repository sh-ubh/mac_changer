#!/usr/bin/env python
#optparse is more declarative type of command line
#re is use to match the string of given regular expression
import subprocess
import optparse
import re

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="inter", help="Give interface to change its mac")
    parser.add_option("-m", "--mac", dest="new", help="Enter new mac address")
    (options, arguments) = parser.parse_args()
    if not options.inter:
        parser.error("[-] Please specify an interface, Use --help for more info.")
    elif not options.new:
        parser.error("[-] Please specify a new mac, Use --help for more info.")

    return options
def change_mac(interface, new_mac):
    print("[+]Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_result:
        return mac_result.group(0)
    else:
        print("[-]Could not read MAC address.")

options = get_args()
current_mac = get_current_mac(options.inter)
print("Current MAC =" + str(current_mac))

change_mac(options.inter, options.new)
current_mac = get_current_mac(options.inter)

if current_mac == options.new:
    print("[+]MAC address successfully changed to " + current_mac)
else:
    print("[-]Failed to change MAC address")

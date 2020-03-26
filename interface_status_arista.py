#!/home/czirakim/python/art/bin/python
""" This script is for shutting down unused ports and place them in a quarantine vlan """
import pyeapi
from pprint import pprint
from jsonrpclib import Server
import ssl

# SSL cert unverify
ssl._create_default_https_context = ssl._create_unverified_context

# vars
switches = ['10.0.0.11','10.0.0.12']
""" the 3 types of ports: bridged,trunk,routed """
interface_mode = ['bridged','trunk']
""" notconnect is a port that is down """
state = 'notconnect'

def shutdown_port(m,n):
    try:
        switch = Server("https://admin:admin@"+n+"/command-api")
        response = switch.runCmds(1, ["enable", "configure", "interface " + m ,"shutdown","switchport access vlan 999" ,"switchport mode access"])
    except:
      print("Could not connect to {} to shutdown ports".format(n))

def show_ports(switch):
     node = pyeapi.connect(transport="https", host=switch, username="admin", password="admin", port=None)
     interface_status = node.execute(["show interfaces status "])
     return interface_status

def main():
    for switch in switches:
        try:
             interface_status=show_ports(switch)
        except:
            print("Could not connect to {} to show interfaces".format(switch))
        status = interface_status["result"][0]["interfaceStatuses"]
        for n in status.keys():
            a = status[n]["linkStatus"]
            ifmode = interface_status["result"][0]["interfaceStatuses"][n]["vlanInformation"]["interfaceMode"]
            if a ==  state and "Ethernet" in n and ifmode in interface_mode:
                shutdown_port(n,switch)

if __name__ == '__main__':
    main()

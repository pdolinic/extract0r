#!/usr/bin/env python3

# Description: Spawn a fast TLS-Python3 Server with no interaction to get files out
# Educational / Created in less than an hour for personal-needs
# Author: pdolinic@netways.de, Junior Consultant at NETWAYS Professional Services GmbH. Deutschherrnstr. 15-19 90429 Nuremberg.

# Date 2021-10-01
# Credits:
# - Webserver Solution: https://stackoverflow.com/questions/19705785/python-3-simple-https-server
# - Certificate Gen: https://lunarwatcher.github.io/posts/2020/05/14/setting-up-ssl-with-pihole-without-a-fqdn.html

# GPL2 License, no warranty /merchantability / fitness /
# Not suited for serious deployment, just rapid file exchange 

import http.server, ssl
import os
import socket

def get_input(prompt:str, expected_type=str):
    while True:
        try:
            inp = input(prompt)
            return expected_type(inp)
        except ValueError:
            pass

agreement = get_input("Do you want to install external pip-dependencies? Press y for yes: ", str)

if not "y" in agreement:
    print("Cancelling pip-depenencies")
else:
    os.system("pip3 install ifaddr")
    import ifaddr



# functions
def print_network_info():
    print(f"WAN:\t{os.system('curl ipinfo.io ')}\n") 
#    print(f"Local:\t{local_ip}")
#    print(f"Local Hostname:\t{hostname}\n")
    print("-> https://raw.githubusercontent.com/pdolinic/Purple/main/fast-web.py ")
    print("-> Extraction: curl -k https://localhost:port/filename --output filename\n")
    print("Warning: Potentially insecure - not suited for production - remember to stopp immediately after usage\n")



adapters = ifaddr.get_adapters()

for adapter in adapters:
    print("IPs of network adapter " + adapter.nice_name)
    for ip in adapter.ips:
        print( "   %s/%s" % (ip.ip, ip.network_prefix))


#hostname = socket.gethostname()
#local_ip = socket.gethostbyname(hostname)

if __name__ == "__main__":

    # the following will only be executed when this script
    # isn't loaded as a module

    print_network_info()

    srv_addr = get_input("Serveraddress to listen on: ", str)
    port = get_input("Port to listen on: ", int)

    os.system("openssl req -new -x509 -keyout '/tmp/server.key' -out '/tmp/server.pem' -days 365 -nodes -subj '/OU=Unknown/O=Unknown/L=Unknown/ST=unknown/C=AU'")
    #set permissions with sticky bit for owner only
    os.system("chmod 1700 /tmp/server.key /tmp/server.pem")
   
    server_address = (srv_addr, port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        server_side=True,
        keyfile='/tmp/server.key',
        certfile='/tmp/server.pem',
        ssl_version=ssl.PROTOCOL_TLS
    )

    try:
        httpd.serve_forever()
    except KeyboardInterrupt as e:
        print(str(e))
        print("Stopping.")
    os.system(rm /tmp/server.key /tmp/server.pem)
    httpd.shutdown()

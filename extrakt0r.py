#!/usr/bin/env python3

# Description: Spawn a fast TLS-Python3 Server with no interaction to get files out
# Educational / Python3 Beginner Practice 
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

def adapter_ips():
    print("--------------------------------------------------------------------------------------")
    adapters= os.system("/sbin/ifconfig | awk '/^[a-z]/ { iface=$1 } /inet / { print iface, $2 }'")
    print(adapters)

def print_network_info():
    print("--------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------")
    print(f"WAN:\t{os.system('curl ipinfo.io ')}\n") 
    print("--------------------------------------------------------------------------------------")
    print("-> Extraction1: curl -k https://localhost:port/filename --output filename")
    print("-> Extraction2: wget -r --no-check-certificate https://localhost:port/")
    print("--------------------------------------------------------------------------------------")
    print("     https://github.com/pdolinic/extrakt0r/blob/main/extrakt0r.py"    )
    print("--------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------")
    print("Warning: Potentially insecure - not suited for production - remember to stopp immediately after usage\n")

if __name__ == "__main__":
    if os.name != 'nt':
    # the following will only be executed when this script
    # isn't loaded as a module
        adapter_ips()
        print_network_info()
        srv_addr = get_input("Serveraddress to listen on: ", str)
        port = get_input("Port to listen on: ", int)

        os.system("openssl req -new -x509 -keyout '/tmp/server.key' -out '/tmp/server.pem' -days 365 -nodes -subj '/OU=%s/O=%s/L=%s/ST=%s/C=XO'" % ('srv_addr','srv_addr','srv_addr','srv_addr'))
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
        httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt as e:
            print(str(e))
            print("Stopping.")
        os.system("rm /tmp/server.key /tmp/server.pem")
        httpd.shutdown()

    else:
        pass

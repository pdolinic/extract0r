#Description: Spawn a fast TLS-Python3 Server with no interaction to get files out

#Educational / Created in less than an hour for personal-needs
#Author: pdolinic@netways.de, Junior Consultant at NETWAYS Professional Services GmbH. Deutschherrnstr. 15-19 90429 Nuremberg.

#Date 2021-10-01
#Credits:
# Webserver Soltuion: https://stackoverflow.com/questions/19705785/python-3-simple-https-server
# Certificate Gen: https://lunarwatcher.github.io/posts/2020/05/14/setting-up-ssl-with-pihole-without-a-fqdn.html

#GPL2 License, no warranty /merchantability / fitness /
#Not suited for serious deployment, just rapid file exchange 

import os
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print("WAN: ")
print(os.system("curl ipinfo.io ")) 
print()
print ("Local: "+ local_ip )
print ("Hostname: " + hostname)
print()
print(" https://raw.githubusercontent.com/pdolinic/Purple/main/fast-web.py ")
print(" Extraction:  curl -k https://localhost:port/filename --output filename ")
print()
print("Warning: Potentially insecure - not suited for production - remember to stopp immediately after usage")

port = int(input("Port to listen on:"))

certValidityDays=1

os.system("openssl req -new -x509 -keyout '../server.key' -out '../server.pem' -days 365 -nodes -subj '/OU=Unknown/O=Unknown/L=Unknown/ST=unknown/C=AU'")

import http.server, ssl

server_address = ('localhost', port)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               keyfile='../server.key',
                               certfile='../server.pem',
                               ssl_version=ssl.PROTOCOL_TLS)
httpd.serve_forever()

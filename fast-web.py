#!/usr/bin/env python3

# Description: Spawn a fast TLS-Python3 Server with no interaction to get files out
# Educational / Python3 Beginner Practice 
# Author: pdolinic@netways.de, Junior Consultant at NETWAYS Professional Services GmbH. Deutschherrnstr. 15-19 90429 Nuremberg.
# Author: Julian Müller (W13R) - w13r.net - https://github.com/W13R

# Date 2021-11-08
# Credits:
# - Webserver Solution: https://stackoverflow.com/questions/19705785/python-3-simple-https-server
# - Certificate Gen: https://lunarwatcher.github.io/posts/2020/05/14/setting-up-ssl-with-pihole-without-a-fqdn.html

# GPL2 License, no warranty /merchantability / fitness /
# Not suited for serious deployment, just rapid file exchange 

import os
import string

from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

from sanic import response
from sanic import Sanic


# variables

scriptDir = Path(__file__).parent
tmpDir = scriptDir / "tmp"
defaultFilesDir = scriptDir / "files"


# helpers 

def get_input(prompt:str, expected_type=str):
    while True:
        try:
            inp = input(prompt)
            return expected_type(inp)
        except ValueError:
            pass

def dependency_check():
    if not "y" in agreement:
       # print("Cancelling pip-depenencies")
         return
    else:
         os.system("pip3 install ifaddr sanic")
         import ifaddr
         adapters = ifaddr.get_adapters()
         for adapter in adapters:
             print("IPs of network adapter " + adapter.nice_name)
             for ip in adapter.ips:
                 print( "   %s/%s" % (ip.ip, ip.network_prefix))

def print_network_info():
    print(f"WAN:\t{os.system('curl ipinfo.io ')}\n") 
    print("-> https://raw.githubusercontent.com/pdolinic/Purple/main/fast-web.py ")
    print("-> Extraction1: curl -k https://localhost:port/filename --output filename")
    print("-> Extraction2: wget -r https://localhost:port/")
    print("Warning: Potentially insecure - not suited for production - remember to stopp immediately after usage\n")


# file server class

class HTTPFileServer:

    filelisting_folder_svg = """
<svg
   width="32"
   height="32"
   viewBox="0 0 32 32"
   version="1.1"
   id="svg5"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs2" />
  <g
     id="layer1">
    <path
       style="fill:#ffd924;fill-opacity:1;stroke:#ce9900;stroke-width:2;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 2,12 V 26 H 30 V 10 H 16 L 12,6 H 2 Z"
       id="path859" />
  </g>
</svg>
    """

    filelisting_file_svg = """
<svg
   width="32"
   height="32"
   viewBox="0 0 32 32"
   version="1.1"
   id="svg5"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs2" />
  <g
     id="layer1">
    <path
       style="display:inline;fill:#ffffff;fill-opacity:1;stroke:#999999;stroke-width:2;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="M 6,6 V 30 H 26 V 9 L 19,2 H 6 Z"
       id="path859" />
    <path
       style="display:inline;fill:#999999;fill-opacity:1;stroke:#999999;stroke-width:2;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"
       d="m 18,2 v 8 h 8 z"
       id="path1770" />
  </g>
</svg>
    """

    filelisting_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Purple HTTP File Server</title>
</head>
<body>
    <style>
        {style}
    </style>
    <div class="currentDirectory">{current_dir}</div>
    <table class="fileListingContainer">
        <tr>
            <th>Name</th>
            <th>Size</th>
            <th>Last modified</th>
        </tr>
        {filelisting}
    </table>
</body>
</html>
    """

    filelisting_style = """
:root {
    --fg-color: #f3f3f3;
    --bg-color: #271c2b;
    --table-bg-color-1: #ffffff10;
    --table-bg-color-2: #ffffff30;
}
body {
    margin: 0;
    width: 100vw;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    background-color: var(--bg-color);
    color: var(--fg-color);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.currentDirectory {
    padding: 1rem .5rem;
    box-sizing: border-box;
    text-align: center;
}
.fileListingContainer, .currentDirectory {
    min-width: 70vw;
    width: fit-content;
    max-width: 50rem;
}
.fileListingContainer {
    border-collapse: collapse;
}
.fileListingContainer tr > td:first-child, .fileListingContainer tr > th:first-child {
    min-width: 50%;
    text-align: left;
}
.fileListingContainer tr {
    background-color: var(--table-bg-color-1);
}
.fileListingContainer tr:nth-child(even) {
    background-color: var(--table-bg-color-2);
}
.fileListingContainer td:first-child {
    padding-left: .8rem;
}
tr {
    padding-left: .5rem;
    padding-right: .5rem;
}
td, th {
    text-align: right;
}
th {
    padding: .5rem .5rem;
}
td {
    padding: .3rem .5rem;
}
td > a {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
}
td > a > svg {
    height: 1.2rem;
    width: auto;
    margin-right: .5rem;
}
a {
    color: var(--fg-color);
}
@media only screen and (max-width: 750px) {
    .fileListingContainer, .currentDirectory {
        min-width: 95vw;
        width: 95vw;
        max-width: 95vw;
    }
    .fileListingContainer tr > td:first-child, .fileListingContainer tr > th:first-child {
        min-width: 30%;
    }
}
    """

    path_allowed_characters = string.ascii_letters + string.digits + string.punctuation + " " + "äÄöÖüÜß"

    def __init__(self, document_root=defaultFilesDir, host="0.0.0.0", port=8005, ssl_cert_path=None, ssl_key_path=None):

        self.document_root = Path(document_root)
        self.host = host
        self.port = port
        self.ssl_key_path = ssl_key_path
        self.ssl_cert_path = ssl_cert_path

        self.sanic = Sanic("Purple HTTP File Server")

        @self.sanic.get("/favicon.ico")
        async def favicon(request):
            return response.empty()

        # requests
        @self.sanic.get("<filepath_:path>")
        async def default_requesthandler(request, filepath_):
            # escape path
            filepath_ = self.escape_path(filepath_)
            # build path
            filepath = self.document_root / filepath_
            print(f"{request.ip}: '{filepath}'")
            # prevent path traversal
            if not filepath.resolve().is_relative_to(self.document_root):
                print(" -> WARNING: Prevented path traversal!")
                return response.text("Forbidden!", status=403)
            # check path
            if not filepath.exists():
                print(" -> Not found!")
                return response.text("Not found!", status=404)
            if filepath.is_symlink():
                print(" -> WARNING: Won't follow symlink!")
                return response.text("Forbidden!", status=403)
            if filepath.is_dir():
                print(" -> directory listing")
                return response.html(self.build_filelisting_html(filepath, filepath_))
            else:
                print(" -> file")
                return await response.file(filepath)
    

    def escape_path(self, path):
        escaped = ""
        for c in repr(path).strip("'"):
            if c in self.path_allowed_characters:
                escaped += unquote(c)
            else:
                escaped += c
        return escaped
    

    def build_filelisting_html(self, absolute_path, relative_path) -> str:

        filelisting_elements = []

        directory_content = Path(absolute_path).glob("*")
        dir_dirs = []
        dir_files = []

        for c in directory_content:
            if c.is_dir():
                dir_dirs.append(c)
            else:
                dir_files.append(c)

        if not relative_path in ("", "/"):
            filelisting_elements.append(f"""
                <tr>
                    <td>
                        <a href='../'>{self.filelisting_folder_svg} <div>../</div></a>
                    </td>
                    <td></td>
                    <td></td>
                </tr>
            """)
        
        for c in sorted(dir_dirs):
            filelisting_elements.append(f"""
                <tr>
                    <td>
                        <a href='{c.name}/'>{self.filelisting_folder_svg} <div>{c.name}/</div></a>
                    </td>
                    <td></td>
                    <td>{datetime.fromtimestamp((c.stat().st_mtime)).strftime("%H:%M %d.%m.%Y")}</td>
                </tr>
            """)
        
        for f in sorted(dir_files):
            filelisting_elements.append(f"""
                <tr>
                    <td>
                        <a href='{f.name}'>{self.filelisting_file_svg} <div>{f.name}</div></a>
                    </td>
                    <td>{f.stat().st_size}</td>
                    <td>{datetime.fromtimestamp((f.stat().st_mtime)).strftime("%H:%M %d.%m.%Y")}</td>
                </tr>
            """)
        return self.filelisting_template.format(
            style = self.filelisting_style,
            current_dir = "/" + relative_path.__str__(),
            filelisting = "\n".join(filelisting_elements)
        )
    

    def run(self):
        if None in (self.ssl_cert_path, self.ssl_key_path):
            self.sanic.run(host=self.host, port=self.port)
        else:
            self.sanic.run(host=self.host, port=self.port, ssl={"cert": self.ssl_cert_path, "key": self.ssl_key_path})



if __name__ == "__main__":

    # the following will only be executed when this script
    # isn't loaded as a module

    agreement = get_input("Do you want to install external pip-dependencies? Press y for yes: ", str)
    dependency_check()

    if os.name != 'nt':

        print_network_info()
        srv_addr, port = (get_input("Serveraddress to listen on: ", str), get_input("Port to listen on: ", int))

        if not tmpDir.exists():
            tmpDir.mkdir()
        
        if not defaultFilesDir.exists():
            defaultFilesDir.mkdir()

        ssl_cert_path = tmpDir / "server.pem"
        ssl_key_path = tmpDir / "server.key"

        # Generate SSL certificate
        os.system(
            "openssl req -new -x509 " +
            f"-keyout '{ssl_key_path.absolute().__str__()}' -out '{ssl_cert_path.absolute().__str__()}' " + 
            "-days 365 -nodes -subj '/OU=Unknown/O=Unknown/L=Unknown/ST=unknown/C=AU'"
        )
        # set permissions with sticky bit for owner only
        os.system(f"chmod 1700 '{ssl_key_path.absolute().__str__()}' '{ssl_cert_path.absolute().__str__()}'")

        httpfileserver = HTTPFileServer(
            host=srv_addr,
            port=port,
            ssl_cert_path=ssl_cert_path.absolute(),
            ssl_key_path=ssl_key_path.absolute()
        )

        httpfileserver.run()

    else:

        print("This operating system is not supported at the moment.")
        exit(1)

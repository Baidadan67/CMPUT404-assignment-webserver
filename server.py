#  coding: utf-8 
import socketserver
from urllib import response

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
         
        self.data = self.data.decode('utf-8')
        d = self.data.split(' ')
        # print(d[1])
        if d[0] != 'GET':
            self.not_allowed()
             
        else:
            self.valid_method(d[1])
        
        self.request.sendall(bytearray("OK",'utf-8'))
    
    def not_allowed(self):
        response = 'HTTP/1.1 405 Method Not Allowed\r\n'
        self.request.send(response.encode('utf-8'))
    
    def valid_method(self, path):  
        if path[-1] != '/' and path[-4: ] != 'html' and path[-3: ]!= 'css': 
            self.redirect(path)
        elif path[-1] == '/':
            path += 'index.html'  
 
        try:
            file = open(f'./www{path}', 'r') 
            data = file.read()
            file.close()
        except:
            headers = f'HTTP/1.1 404 Not Found\r\n'  
            self.request.send(headers.encode('utf-8'))
            return
        
        content_type =  path[-4:].split('.')[0] or path[-4:].split('.')[1] 
        headers = f'HTTP/1.1 200 OK\r\nContent-Type:text/{content_type}\r\nContent-Length:{len(data)}\r\n\r\n{data}'

        self.request.send(headers.encode('utf-8'))
         
    
    def redirect(self, path): 
         
        response = f'HTTP/1.1 301 Moved Permanently\r\nLocation:{path+"/"}\r\n' 
        self.request.send(response.encode('utf-8'))
        
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

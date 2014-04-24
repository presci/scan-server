#!/usr/bin/python

import os
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

PORT_NUMBER = 9093
SCANCOMMAND="/home/prasad/Workspace/scan-server/scanimage.sh"
SCANSTOP="kill $(ps aux | grep scanimage | grep device | awk '{print $2}')"
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path="/index.html"
        try:
            sendReply = False
            if self.path.endswith("scan"):
                print "found request"
                os.system(SCANCOMMAND)
                sendReply = True
            elif self.path.endswith('scanstop'):
                print 'stopping scan'
                os.system(SCANSTOP)
                sendReply = True
            if sendReply == True:
                self.send_response(204)
                self.end_headers()
            return
        except IOError:
            self.send_error(404, 'File not found %s' % self.path)


try:
    server = HTTPServer(('', PORT_NUMBER), MyHandler)
    print "Started Server at port ", PORT_NUMBER
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
        

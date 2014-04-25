#!/usr/bin/python

import os
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import ConfigParser

PORT_NUMBER = 9093
SCANCOMMAND="/home/prasad/Workspace/scan-server/scanimage.sh"
SCANSTOP="kill $(ps aux | grep scanimage | grep device | awk '{print $2}')"

class MyHandler(BaseHTTPRequestHandler):
    def __init__(self):
        super(MyHandler, sefl).__init__()
        self.config = ConfigParser.ConfigParser()
        self.config.read('scanserver.ini')
    def serve(self, path, restype='text/html'):
        f=open('static' + path)
        self.send_response(200)
        self.send_header('Content-type', restype)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        return
    def do_GET(self):
        print self.path
        if self.path.endswith('html'):
            self.serve(self.path)
            return
        if self.path.endswith('js'):
            self.serve(self.path, 'application/javascript')
            return
        try:
            sendReply = False
            if self.path.endswith('token'):
                print self.path
                return
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
        

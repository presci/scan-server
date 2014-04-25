#!/usr/bin/python

import os
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import ConfigParser
import urlparse
import json
from StringIO import StringIO
import os


PORT_NUMBER = 9093
SCANCOMMAND="/home/prasad/Workspace/scan-server/scanimage.sh"
SCANSTOP="kill $(ps aux | grep scanimage | grep device | awk '{print $2}')"

class MyHandler(BaseHTTPRequestHandler):
    def serve(self, path, restype='text/html'):
        f=open('static' + path)
        self.send_response(200)
        self.send_header('Content-type', restype)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
        return
    def dumpjson(self, data):
        io = StringIO()
        json.dump(data, io)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(io.getvalue())
        return
    def handlerequest(self):
        K=urlparse.urlparse(self.path)
        if K.path.endswith('token'):
            query=dict(urlparse.parse_qsl(K.query))
            self.code=query['code']
            self.serve('/dir.html')
            return False
        if K.path.endswith('dir.json'):
            count = 5
            if K.query != '':
                query=dict(urlparse.parse_qsl(K.query))
                count=int(query['count'])
            dirs=[d for d in os.listdir('/Users/piyer/windows/workspace/') if os.path.isdir(os.path.join('/Users/piyer/windows/workspace/', d))]
            d=sorted(dirs, key=lambda x: os.path.getctime(), reverse=True)[:count]
            self.dumpjson(d)
            return False
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
            if self.path.endswith("scan"):
                print "found request"
                os.system(SCANCOMMAND)
                sendReply = True
            if self.path.endswith('scanstop'):
                print 'stopping scan'
                os.system(SCANSTOP)
                sendReply = True
            if self.path.endswith('test'):
                sendReply = True
            else :
                sendReply=self.handlerequest()
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
        

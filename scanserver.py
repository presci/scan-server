#!/usr/bin/python

import os
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import ConfigParser
import urlparse
import json
from StringIO import StringIO
import os
from Cookie import SimpleCookie as cookie
from uuid import uuid4 as uuid
from time import time as time
import sqlite3


PORT_NUMBER = 9093
SCANCOMMAND="/home/prasad/Workspace/scan-server/scanimage.sh"
SCANSTOP="kill $(ps aux | grep scanimage | grep device | awk '{print $2}')"





class MyHandler(BaseHTTPRequestHandler):
    sessioncookies={}

    def __init__(self, *args, **Kwargs):
        self.sessionidmorsel = None
        BaseHTTPRequestHandler.__init__(self, *args, **Kwargs)

    def _session_cookie(self, code=None,forcenew=False):
        m='session_id'
        cookiestring = self.headers.getheader('Cookie')
        if cookiestring is None:
            cookiestring=''
        c = cookie()
        c.load(cookiestring)
        _uuid= uuid().hex
        if forcenew or self.sessioncookies:
            c[m] = _uuid
            conn.execute('insert into uid_code(uid, code) values("%s", "%s")'%(_uuid, code))
        else :
            _uuid = c.get('m', _uuid)
        c[m] = _uuid
        c[m]['httponly'] = True
        c[m]['max-age'] = 3600
        c[m]['expires']=self.date_time_string(time() + 3600)
        return (_uuid, c[m].OutputString())

    def serve(self, path,  code=None, forceNew=False, restype='text/html'):
        f=open('static' + path)
        self.send_response(200)
        self.send_header('Content-type', restype)
        _cookie = self._session_cookie(code, forceNew)
        self.send_header('Set-Cookie', _cookie[1])
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

    def upload(self, data):
        filelines=[]
        for K in data:
            with open(K) in file:
                for lines in file:
                    filelines.append(lines)
        for J in filelines:
            print filelines

    def handlerequest(self):
        K=urlparse.urlparse(self.path)
        self._session_cookie()

        if K.path.endswith('token'):
            query=dict(urlparse.parse_qsl(K.query))
            code=query['code']
            self.serve('/index.html', code, True)
            return False
        if K.path.endswith('dir.json'):
            count = 5
            if K.query != '':
                query=dict(urlparse.parse_qsl(K.query))
                count=int(query['count'])
            dirs=[d for d in os.listdir('/Users/piyer/windows/workspace/') if os.path.isdir(os.path.join('/Users/piyer/windows/workspace/', d))]
            dirs=[os.path.join('/Users/piyer/windows/workspace', d) for d in dirs]
            d=sorted(dirs, key=lambda x: os.path.getctime(x), reverse=True)[:count]
            self.dumpjson(d)
            return False

    def do_GET(self):
        if self.path.endswith('html'):
            self.serve(path=self.path)
            return
        if self.path.endswith('js'):
            self.serve(path=self.path, restype='application/javascript')
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

    def do_POST(self):
        if  self.path.endswith('upload.json'):
            self._session_cookie()
            content_len = int(self.headers.getheader('content-length'))
            post_body = self.rfile.read(content_len)
            K=json.loads(post_body)
            #if 'dir' in K:
            #    if len(K['dir']) > 0:
            #        self.upload(K['dir'])
            #self.send_response(204)
            #self.end_headers()
        else:
            print self.path
            self.send_response(204)
            self.end_headers()



conn = sqlite3.connect(':memory:')
conn.execute('create table uid_code(uid, code)')
    
try:
    server = HTTPServer(('', PORT_NUMBER), MyHandler)
    print "Started Server at port ", PORT_NUMBER
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
        

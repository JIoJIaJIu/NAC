#/usr/bin/env python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from nn.tools import train

PORT = 8000

def Home(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write('Hello world')

def E404(self):
    self.send_response(404)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write('Unsupported url %s' % self.path)

GET_CNTRLS = {
    '/': Home,
    '404': E404,
}

def Data(self):
    pass

def Forbidden(self):
    self.send_response(400)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write('Unsupported url %s' % self.path)

POST_CNTRLS = {
    '/data': Data,
    '400': Forbidden,
}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not GET_CNTRLS.has_key(self.path):
            return GET_CNTRLS['404'](self)

        GET_CNTRLS[self.path](self)

    def do_POST(self):
        if not POST_CNTRLS.has_key(self.path):
            return POST_CNTRLS['400'](self)
        POST_CNTRLS[self.path](self)

httpd = HTTPServer(('', PORT), Handler)

print 'Start NN'
print 'Wait..'
train()

print 'Server has been started on PORT :%d' % PORT
httpd.serve_forever()

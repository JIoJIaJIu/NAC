from pyramid.config import Configurator
from pyramid.response import Response
from wsgiref.simple_server import make_server

PORT = 8000
if __name__ == '__main__':
    config = Configurator()
    config.add_static_view('', path='./public')

    app = config.make_wsgi_app()

    print 'Server has been started on PORT :%d' % PORT
    server = make_server('', PORT, app)
    server.serve_forever()

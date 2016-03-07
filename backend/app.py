from pyramid.config import Configurator
from pyramid.response import Response
from wsgiref.simple_server import make_server
from nn.tools import train, load_kdd_names 
from nn.ids import PacketFactory
import json
import sys

[attacks, names] = load_kdd_names()

PORT = 8000
net = None 
def upload(req):
    data = req.POST['mcap'].file.read()
    data = json.loads(data)
    factory = PacketFactory(names)
    response = []
    for row in data:
        p = factory.create_packet(row)
        response.append(net.activate(p.get_data())[0])
    #TODO;
    return Response('<br/>'.join(map(lambda x: str(x), response)))


if __name__ == '__main__':
    global net

    try:
        if sys.argv.index('--v2'):
            v2 = True
    except Exception:    
        v2 = False
        print 'You may use `--v2` option to load another data set'

    config = Configurator()
    config.add_route('upload', '/upload')
    config.add_view(upload, route_name='upload')
    config.add_static_view('', path='./public')

    print 'Start NN'
    print 'Wait..'
    [net, _] = train(v2)

    app = config.make_wsgi_app()

    print 'Server has been started on PORT :%d' % PORT
    server = make_server('', PORT, app)
    server.serve_forever()

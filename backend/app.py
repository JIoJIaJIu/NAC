from pyramid.config import Configurator
from pyramid.response import Response
from wsgiref.simple_server import make_server
from nn.tools import train, load_kdd_names 
from nn.ids import PacketFactory
import json
import sys

PORT = 8000
net = None 
v2 = False

def upload(req):
    [attacks, names] = load_kdd_names(v2)

    data = req.POST['file'].file.read()
    data = json.loads(data)
    factory = PacketFactory(names)
    response = []

    for row in data:
        p = factory.create_packet(row)
        response.append(net.activate(p.get_data())[0])

    class_index = round(max(response))
    print class_index, response

    class_name = attacks[class_index]
    hasIntrusion = class_name 
    return Response(json.dump({'hasIntrusion': hasIntrusion}))


if __name__ == '__main__':
    global net
    global v2

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

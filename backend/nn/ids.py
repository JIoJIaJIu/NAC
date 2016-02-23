#from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer
import urllib2
import os
from os.path import join
import json
from scapy.all import Raw
from pybrain.structure import *

def create_net(DS):
    inLayer = LinearLayer(DS.indim)
    hidden1Layer = SigmoidLayer(3)
    hidden2Layer = SigmoidLayer(3)
    hidden3Layer = SigmoidLayer(4)
    outLayer = SigmoidLayer(DS.outdim)

    net = FeedForwardNetwork()
    net.addInputModule(inLayer)
    for layer in [hidden1Layer, hidden2Layer, hidden3Layer]:
        net.addModule(layer)
    net.addOutputModule(outLayer)

    in_to_hidden1 = FullConnection(inLayer, hidden1Layer)
    hidden1_to_hidden2 = FullConnection(hidden1Layer, hidden2Layer)
    hidden2_to_hidden3 = FullConnection(hidden2Layer, hidden3Layer)
    hidden3_to_out = FullConnection(hidden3Layer, outLayer)
    net.addConnection(in_to_hidden1)
    net.addConnection(hidden1_to_hidden2)
    net.addConnection(hidden2_to_hidden3)
    net.addConnection(hidden3_to_out)

    net.sortModules()
    return net

class PacketFactory(object):
    flags = json.load(open(join(os.getcwd(), './data/flags.json')))
    services = json.load(open(join(os.getcwd(), './data/services.json')))

    def __init__(self, names):
        self.names = names

    def create_packet(self, data):
        return PacketData(data, self.names)

    @classmethod
    def convert_protocol_type(cls, data):
        return {
            'udp': 0,
            'tcp': 1,
            'icmp': 2,
        }[data]

    @classmethod
    def convert_service(cls, data):
        return cls.services[data]

    @classmethod
    def convert_flag(cls, data):
        return cls.flags[data]

class PacketData(object):
    def __init__(self, datas, names):
        self.data = {}

        for (i, data) in enumerate(datas):
            key = names[i]
            self.data[key] = self.convert(key, data)

    def get_data(self):
        return self.data.values()

    def convert(self, key, data):
        fns = {
            'protocol_type': lambda: PacketFactory.convert_protocol_type(data),
            'service': lambda: PacketFactory.convert_service(data),
            'flag': lambda: PacketFactory.convert_flag(data),
        }

        if fns.has_key(key):
            data = fns[key]()
        return data

    def __str__(self):
        return self.data.__str__()

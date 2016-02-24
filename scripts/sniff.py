#!/usr/bin/env python
from scapy.all import sniff
import os
import time
import utils 
import json

import scapy

def _sniff():
   print 'Sniffing..'
   p = sniff(store=1) 
   print 'Stop'
   file_name = 'packets.%s.mpcap' % int(time.time()) 
   p = normalize(p)
   return
   fd = open(file_name, 'w')
   fd.write(p)
   print 'Output in %s' % file_name


def normalize(p):
    data = []
    ranges = count_ranges(p)
    for r in ranges:
        data.append(normalize_range(r))
    return json.dumps(data)

def count_ranges(p):
    [an, un] = p.sr()
    ranges = []
    for ask, res in an:
        ask = packet_to_layers(ask)
        res = packet_to_layers(res)

        ranges.append([ask, res])
    return ranges
    
def packet_to_layers(packet):
    i = 0
    layers = {}

    while True:
        layer = packet.getlayer(i)
        if not layer:
            break
        layer_name = layer.name
        layers[layer.name] = layer
        i += 1

    return layers


def normalize_range(ranges):
    [ask, res] = ranges
    return {
        'duration': utils.count_duration(ask, res), #continuous.
        'protocol_type': utils.get_protocol(ask), #symbolic.
        'service': utils.get_service(ask), #symbolic.
        'flag': utils.get_flag(ask), #symbolic. 
        'src_bytes': utils.get_src_bytes(ask), #continuous.
        'dst_bytes': utils.get_dst_bytes(res), #continuous.
        'land': 0, #symbolic.
        'wrong_fragment': 0, #continuous.
        'urgent': 0, #continuous.
        'hot': 0, #continuous.
        'num_failed_logins': 0, #continuous.
        'logged_in': 0, #symbolic.
        'num_compromised': 0, #continuous.
        'root_shell': 0, #continuous.
        'su_attempted': 0, #continuous.
        'num_root': 0, #continuous.
        'num_file_creations': 0, #continuous.
        'num_shells': 0, #continuous.
        'num_access_files': 0, #continuous.
        'num_outbound_cmds': 0, #continuous.
        'is_host_login': 0, #symbolic.
        'is_guest_login': 0, #symbolic.
        'count': 0, #continuous.
        'srv_count': 0, #continuous.
        'serror_rate': 0, #continuous.
        'srv_serror_rate': 0, #continuous.
        'rerror_rate': 0, #continuous.
        'srv_rerror_rate': 0, #continuous.
        'same_srv_rate': 0, #continuous.
        'diff_srv_rate': 0, #continuous.
        'srv_diff_host_rate': 0, #continuous.
        'dst_host_count': 0, #continuous.
        'dst_host_srv_count': 0, #continuous.
        'dst_host_same_srv_rate': 0, #continuous.
        'dst_host_diff_srv_rate': 0, #continuous.
        'dst_host_same_src_port_rate': 0, #continuous.
        'dst_host_srv_diff_host_rate': 0, #continuous.
        'dst_host_serror_rate': 0, #continuous.
        'dst_host_srv_serror_rate': 0, #continuous.
        'dst_host_rerror_rate': 0, #continuous.
        'dst_host_srv_rerror_rate': 0 #continuous.
    }

if __name__ == '__main__':
    _sniff()

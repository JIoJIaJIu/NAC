#!/usr/bin/env python
from scapy.all import sniff
import os
import time
import utils
import json

import scapy

def _sniff():
   print 'Sniffing..'
   p = sniff(prn=lambda p: p.summary())
   print 'Stop'
   file_name = 'packets.%s.mpcap' % int(time.time())
   p = normalize(p)
   fd = open(file_name, 'w')
   fd.write(p)
   print 'Output in %s' % file_name


# normalize packets range for nn format
def normalize(p):
    data = []
    frames = build_frames(p)
    # skip unknow protocol
    frames = filter(lambda f: f[1] != 'unknown', frames)
    return json.dumps(frames)

# trasform raw packets in 2sec frame
def build_frames(p):
    (ans, unans) = p.sr()

    frames = []

    for s, r in ans:
        frame = build_frame(s, r)
        frames.append(frame)

    for p in unans:
        frame = build_frame_from_single(p)
        frames.append()
    return frames


def build_frame(r, s):
    r_layers = format_packet_to_layers(r)
    s_layers = format_packet_to_layers(s)
    frame = [
        utils.count_duration(r_layers, s_layers), #duration: continuous
        utils.get_protocol(r), #protocol_type': #symbolic
        utils.get_service(r, s), #service: #symbolic.
        utils.get_flag(r, s), #flag: #symbolic.
        utils.get_src_bytes(r), #src_bytes: #continuous.
        utils.get_dst_bytes(s), #dst_bytes': #continuous.
        utils.is_land(r), #land: #symbolic.
        0, #wrong_fragment: #continuous.
        0, #urgent: #continuous.
        0, #hot: #continuous
        0, #num_failed_logins: #continuous.
        0, #logged_in: #symbolic.
        0, #num_compromised: #continuous.
        0, #root_shell: #continuous.
        0, #su_attempted: #continuous.
        0, #num_root: #continuous.
        0, #num_file_creations: #continuous.
        0, #num_shells: #continuous.
        0, #num_access_files: #continuous.
        0, #num_outbound_cmds: #continuous.
        0, #is_host_login: #symbolic.
        0, #is_guest_login: #symbolic
        0, #count: #continuous.
        0, #srv_count: #continuous.
        0, #serror_rate: #continuous.
        0, #srv_serror_rate: #continuous.
        0, #rerror_rate: #continuous.
        0, #srv_rerror_rate: #continuous
        0, #same_srv_rate: #continuous
        0, #diff_srv_rate: #continuous
        0, #srv_diff_host_rate: #continuous
        0, #dst_host_count: #continuous
        0, #dst_host_srv_count: #continuous
        0, #dst_host_same_srv_rate: #continuous
        0, #dst_host_diff_srv_rate: #continuous
        0, #dst_host_same_src_port_rate: #continuous
        0, #dst_host_srv_diff_host_rate: #continuous.
        0, #dst_host_serror_rate: #continuous
        0, #dst_host_srv_serror_rate: #continuous
        0, #dst_host_rerror_rate: #continuous
        0 #dst_host_srv_rerror_rate: #continuous
    ]

    return frame

def build_frame_from_single(p):
    frame = [
        0, #duration: continuous
        utils.get_protocol(p), #protocol_type': #symbolic
        utils.get_service(p), #service: #symbolic.
        utils.get_flag(p), #flag: #symbolic.
        utils.get_src_bytes(p), #src_bytes: #continuous.
        utils.get_dst_bytes(p), #dst_bytes: #continuous.
        utils.is_land(p), #land: #symbolic.
        0, #wrong_fragment: #continuous.
        0, #urgent: #continuous.
        0, #hot: #continuous
        0, #num_failed_logins: #continuous.
        0, #logged_in: #symbolic.
        0, #num_compromised: #continuous.
        0, #root_shell: #continuous.
        0, #su_attempted: #continuous.
        0, #num_root: #continuous.
        0, #num_file_creations: #continuous.
        0, #num_shells: #continuous.
        0, #num_access_files: #continuous.
        0, #num_outbound_cmds: #continuous.
        0, #is_host_login: #symbolic.
        0, #is_guest_login: #symbolic
        0, #count: #continuous.
        0, #srv_count: #continuous.
        0, #serror_rate: #continuous.
        0, #srv_serror_rate: #continuous.
        0, #rerror_rate: #continuous.
        0, #srv_rerror_rate: #continuous
        0, #same_srv_rate: #continuous
        0, #diff_srv_rate: #continuous
        0, #srv_diff_host_rate: #continuous
        0, #dst_host_count: #continuous
        0, #dst_host_srv_count: #continuous
        0, #dst_host_same_srv_rate: #continuous
        0, #dst_host_diff_srv_rate: #continuous
        0, #dst_host_same_src_port_rate: #continuous
        0, #dst_host_srv_diff_host_rate: #continuous.
        0, #dst_host_serror_rate: #continuous
        0, #dst_host_srv_serror_rate: #continuous
        0, #dst_host_rerror_rate: #continuous
        0 #dst_host_srv_rerror_rate: #continuous
    ]
    return frame

# format packet in layers dict
def format_packet_to_layers(packet):
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

if __name__ == '__main__':
    _sniff()

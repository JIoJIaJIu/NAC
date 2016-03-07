# -*- coding: utf8 -*-
import json

services = json.load(open('../backend/data/services.json'))
def count_duration(ask, res):
    if not ask.has_key('TCP') or not res.has_key('TCP'):
        return 0
    delta = res['TCP'].time - ask['TCP'].time
    return delta

def get_protocol(p):
    if p.haslayer('TCP'):
        return 'tcp'
    elif p.haslayer('ICMP'):
        return 'icmp'
    elif p.haslayer('UDP'):
        return 'udp'

    return 'unknown'

# Return available services:
# http
# domain
# http_443
#
def get_service(r, s):
    print '--' * 30
    print r.show() ,'\n\n', s.show()
    if r.haslayer('TCP'):
        tcp = r['TCP']
        if tcp.dport == 'http':
            return 'http'
        elif tcp.dport == 'https':
            return 'http_443'

    elif r.haslayer('UDP'):
        udp = r['UDP']
        if udp.dport == 'domain':
            return 'domain'
        
    return 'unknown'

# Return flags of connection
# RSTOS0 - Originator sent a SYN followed by a RST, never see a SYN ACK from the responder
# RSTR - Established, responder aborted
# RSTO - Connection established, originator aborted (sent a RST)
# OTH - No SYN seen, just midstream traffic (a “partial connection” that was not later closed)
# REJ - Connection attempt rejected 
# S0 - Connection attempt seen, no reply
# S1 - Connection established, not terminated
# S2 - Connection established and close attempt by originator seen (but no reply from responder)
# S3 - Connection established and close attempt by responder seen (but no reply from originator)
# SF - Normal establishment and termination
# SH - Originator sent a SYN followed by a FIN (finish ‘flag’) , never saw a SYN ACK from the responder (hence the connection was “half” open)

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80

# need to improve
def get_flag(r, s=None):
    if r.haslayer('TCP') and s:
        tcp = r['TCP']
        sflags = tcp.flags
        tcp = s['TCP']
        dflags = tcp.flags
        
        if sflags & RST and sflags & SYN:
            return 'RSTOS0'
    return 'SF'

def get_src_bytes(r):
    return len(r)

def get_dst_bytes(s):
    return len(s)

def is_land(r):
    ip = r['IP']
    return 1 if ip.dst == ip.src else 0

import json

services = json.load(open('../backend/data/services.json'))
def count_duration(ask, res):
    if not ask.has_key('TCP') or not res.has_key('TCP'):
        return 0
    delta = res['TCP'].time - ask['TCP'].time
    return delta

def get_protocol(p):
    if p.has_key('TCP'):
        return 'tcp'
    if p.has_key('ICMP'):
        return 'icmp'

    if p.has_key('udp'):
        return 'udp'

    return 'unknown'

def get_service(p):
    pass

def get_flag(p):
    pass

def get_src_bytes(p):
    pass

def get_dst_bytes(p):
    pass

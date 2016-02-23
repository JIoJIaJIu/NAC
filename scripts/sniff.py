#!/usr/bin/env python
from scapy.all import sniff

import scapy
OUTPUT = 'sniff.pcap'

def _sniff():
   p = sniff(store=1) 
   fd = open(OUTPUT, 'w')
   #fd.write()

if __name__ == '__main__':
    _sniff()

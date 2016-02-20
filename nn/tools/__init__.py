import os
import sys
import urllib
from setuptools import Command

PCAP_URL = 'http://download.netresec.com/pcap/maccdc-2012/maccdc2012_00000.pcap.gz'
PCAP_OUTPUT = './data/maccdc.pcap.gz'

def progress(count, block_size, total):
    percent = int(count * block_size * 100 / total)
    sys.stdout.write("\rdownloading...%d%%" % percent)
    sys.stdout.flush()

def download_pcap():
    realpath = os.path.realpath(PCAP_OUTPUT)
    print realpath
    if os.path.exists(realpath):
        print 'File already downloaded. Delete it by hand if you want to reload it <%s>' % PCAP_OUTPUT
        return
    pcap = urllib.URLopener()
    pcap.retrieve(PCAP_URL, realpath, reporthook=progress)
    print 'Wait for downloading...'

class TrainCommand(Command):
    description = 'Train our neural network'
    user_options = [] 

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        download_pcap()

import os
from os.path import join
import sys
import urllib
import gzip
from itertools import islice
from setuptools import Command
from pybrain.datasets import SupervisedDataSet, ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer

from nn.ids import PacketFactory, create_net

KDD_URL = 'https://web.archive.org/web/20150406000710/http://nsl.cs.unb.ca/NSL-KDD/KDDTest+.txt'
KDD_V2_URL = 'http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data.gz'
KDD_OUTPUT = join(os.getcwd(), './data/kddtrain.arff')
KDD_V2_OUTPUT = join(os.getcwd(), './data/kdd.gz')

KDD_NAMES_URL = 'http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names'
KDD_NAMES_OUTPUT = join(os.getcwd(), './data/kdd.names')

# count of datas
COUNT = 100000
#COUNT = 100

def progress(count, block_size, total):
    percent = int(count * block_size * 100 / total)
    sys.stdout.write("\rdownloading...%d%%" % percent)
    sys.stdout.flush()

def download_kdd(v2=False):
    output = KDD_OUTPUT if not v2 else KDD_V2_OUTPUT
    url = KDD_URL if not v2 else KDD_V2_URL
    realpath = os.path.realpath(output)
    print 'Download %s' % url
    if os.path.exists(realpath):
        print 'File already downloaded. Delete it by hand if you want to reload it <%s>' % output
        return
    kdd = urllib.URLopener()
    kdd.retrieve(url, realpath, reporthook=progress)

def load_kdd_names(v2=False):
    realpath = os.path.realpath(KDD_NAMES_OUTPUT)
    if os.path.exists(realpath):
        print 'File already downloaded. Delete it by hand if you want to reload it <%s>' % KDD_NAMES_OUTPUT
    else:
        print 'Download %s' % KDD_NAMES_URL
        urllib.urlretrieve(KDD_NAMES_URL, KDD_NAMES_OUTPUT)

    datas = open(KDD_NAMES_OUTPUT)
    attacks = datas.readline()[:-2].split(',')

    names = []
    for line in datas.readlines():
        [key, _] = line[:-1].split(':')
        names.append(key)
    names.append('state')
    if not v2:
        attacks = ['normal', 'anomaly']
    return [attacks, names]

class TrainCommand(Command):
    description = 'Train our neural network'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        train()

def train(v2=None):
    print 'Use %s data set' % ('v1' if not v2 else 'v2')
    download_kdd(v2)
    [attacks, names] = load_kdd_names(v2)
    print "Available classes: %s" % ', '.join(attacks)
    DS = ClassificationDataSet(len(names) - 1, nb_classes=len(attacks), class_labels=attacks)

    factory = PacketFactory(names)

    if v2:
        fd = gzip.open(KDD_V2_OUTPUT)
    else:
        fd = open(KDD_OUTPUT)

    with fd as f:
        for line in islice(f, COUNT):
            data = line[:-1].split(',')
            class_name = data[-1]
            # remove trailing .
            if v2:
                class_name = class_name[:-1]
            id = attacks.index(class_name)

            packet = factory.create_packet(data[:-1])
            DS.appendLinked(packet.get_data(), [id])

    net = create_net(DS)
    print 'Start training'
    test, train = DS.splitWithProportion(0.25)
    print "Number of training patterns: ", len(train)
    print "Input and output dimensions: ", train.indim, train.outdim
    print "First sample (input, target, class):"
    print train['input'][0], train['class']
    print train['target'][0]
    print DS.calculateStatistics()
    print DS.classHist

    print '-' * 100
    print net.params

    trainer = BackpropTrainer(net, DS, verbose=True)
    trainer.train()
    print 'Successfull training'
    return [net, DS]

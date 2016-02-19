from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import FeedForwardNetwork

def main():
    net = buildNetwork(2, 3, 1)
    #net = FeedForwardNetwork()
    print(net)

if __name__ == '__main__':
    print 'wtf'

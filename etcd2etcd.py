from datetime import datetime
from urlparse import urlparse
import os
import sys
import commands
import argparse
import etcd

def copy(client, nodes, srckey, destkey):
        for i, node in enumerate(nodes):
        #while(node = nodes.pop()):
                print(node.get('key') + "\tTo\t" + node.get('key').replace(srckey,destkey,1))
                if node.get('dir', False) == True:
                        client.write(key=node.get('key').replace(srckey,destkey,1), value=None, dir=True)
                        copy(client, node.get('nodes'), srckey, destkey)
                else:
                        client.write(key=node.get('key').replace(srckey,destkey,1), value=node.get('value'))

def makeClient(endpoint):
        url = urlparse(endpoint)
        client = etcd.Client(host=url.hostname, port=url.port)
        return client

def parse_args():
        parser = argparse.ArgumentParser(description='etcd-to-etcd copier.')
        parser.add_argument('--source', action="store", dest="src", type=str, required=True, help='Endpoint for source etcd.')
        parser.add_argument('--destination', action="store", dest="dest", type=str, required=True, help='Endpoint for destination etcd.')
        parser.add_argument('--source-key', action="store", dest="srckey", type=str, required=True, help='Key from source.')
        parser.add_argument('--destination-key', action="store", dest="destkey", type=str, required=True, help='Key to destination.')
        args = parser.parse_args()
        return args


def main():
        args = parse_args()
        srcClient = makeClient(args.src)
        destClient = makeClient(args.dest)
        result = srcClient.read(args.srckey, recursive = True)
        if result.dir == True:
                destClient.write(key=args.destkey, value=None, dir=True)
                copy(destClient, result._children, args.srckey, args.destkey)
        else:
                destClient.write(key=args.destkey, value=result.value)
        print(args.srckey + "\tTo\t" + args.destkey)

if __name__ == '__main__':
        main()

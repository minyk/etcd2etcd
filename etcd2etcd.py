from datetime import datetime
from urlparse import urlparse
import os
import sys
import commands
import argparse
import etcd

def copy(client, nodes):
	for i, node in enumerate(nodes):
	#while(node = nodes.pop()):
		if node.get('dir', False) == True:
			client.write(key=node.get('key'), value=None, dir=True)
			copy(client, node.get('nodes'))
		else:
			client.write(key=node.get('key'), value=node.get('value'))

def makeClient(endpoint):
        url = urlparse(endpoint)
	client = etcd.Client(host=url.hostname, port=url.port)
	return client

def parse_args():
	parser = argparse.ArgumentParser(description='etcd-to-etcd copier.')
	parser.add_argument('--source', action="store", dest="src", type=str, required=True, help='Endpoint for source etcd.')
	parser.add_argument('--destination', action="store", dest="dest", type=str, required=True, help='Endpoint for destination etcd.')
	parser.add_argument('--target', action="store", dest="target", type=str, required=True, help='Target key')
	args = parser.parse_args()
	return args


def main():
	args = parse_args()
	srcClient = makeClient(args.src)
	destClient = makeClient(args.dest)
	result = srcClient.read(args.target, recursive = True)
	if result.dir == True:
		destClient.write(key=result.key, value=None, dir=True)
		copy(destClient, result._children)
	else:
		destClient.write(key=result.key, value=result.value)
	#print(keys)

if __name__ == '__main__':
	main()


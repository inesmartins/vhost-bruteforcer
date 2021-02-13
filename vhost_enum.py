import os 
import argparse

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

# parses arguments
parser = argparse.ArgumentParser(description='Brute-forces vhosts for given --ip and based on specified domain and wordlist')
parser.add_argument('-i', '--ip-address', dest='ip', type=str, required=True)
parser.add_argument('-d', '--domain', dest='domain', type=str, required=True)
parser.add_argument('-w', '--wordlist', dest='wordlist', metavar="FILE", type=lambda x: is_valid_file(parser, x), required=True)
parser.add_argument('-s', '--success', dest='success', type=str, required=False)
parser.add_argument('-f', '--failure', dest='failure', type=str, required=False)
parser.add_argument('-o', '--output-file', dest='out_file', metavar='FILE', type=lambda x: is_valid_file(parser, x), required=True)
args = parser.parse_args()

f = open(args.wordlist, "r")
words = f.read().split("\n")
for word in words:
	req = "curl -H \'Host: " + word + "." + args.domain + "\' " + args.ip
	res = os.popen(req).read()
	if args.success != NULL:
		if args.success in res:
			print("Found vhost " + word + "." + args.domain)
			if args.out_file != NULL:
				os.system("echo " + word + "." + args.domain  >> out_file)
	if args.failure != NULL:
		if args.failure not in res:
			print("Found vhost " + word + "." + args.domain)
                        if args.out_file != NULL:
                                os.system("echo " + word + "." + args.domain$

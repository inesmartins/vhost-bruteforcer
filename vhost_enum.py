import os 
import argparse

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

# parses arguments
parser = argparse.ArgumentParser(description='Brute-forces vhosts for given --ip and based on specified domain and wordlist')
parser.add_argument('-i', '--ip-address', dest='ip', type=str, required=True)
parser.add_argument('-d', '--domain', dest='domain', type=str, required=True)
parser.add_argument('-w', '--wordlist', dest='wordlist', metavar="FILE", type=lambda x: is_valid_file(parser, x), required=True)
parser.add_argument('-s', '--success', dest='success', type=str, required=False)
parser.add_argument('-f', '--failure', dest='failure', type=str, required=False)
parser.add_argument('-o', '--output-file', dest='out_file', metavar='FILE', type=str, required=True)
args = parser.parse_args()

if args.success is None and args.failure is None:
	parser.error('Please specify either success (-s/--success) or failure (-f/--failure) content')

f = open(args.wordlist, "r")
words = f.read().split("\n")

for word in words:
	req = "curl -H \'Host: " + word + "." + args.domain + "\' " + args.ip
	res = os.popen(req).read()

	# user specified success page content
	if args.success is not None and args.success in res:
		print("Found vhost " + word + "." + args.domain)
		if args.out_file is not None:
			os.system("echo " + word + "." + args.domain >> args.out_file)

	# user specified error page content
	if args.failure is not None and args.failure not in res:
		print("Found vhost " + word + "." + args.domain)
		if args.out_file is not None:
			os.system("echo " + word + "." + args.domain >> args.out_file)
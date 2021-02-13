import os 
import argparse

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

def nullable_string(val):
    if not val:
        return None
    return val

def found_vhost(vhost, out_file):
	print('Found vhost: ' + vhost)
	if args.out_file is not None:
		os.system('echo ' + vhost + ' >> ' + out_file)

# parses arguments
parser = argparse.ArgumentParser(description='Brute-forces vhosts for given --ip and based on specified domain and wordlist')
parser.add_argument('-i', '--ip-address', 
					dest='ip', 
					help='the IP to bruteforce', 
					type=str, required=True)
parser.add_argument('-d', '--domain', 
					dest='domain', 
					help='the domain that we\'ll use as suffix', 
					type=str, required=True)
parser.add_argument('-w', '--wordlist', 
					dest='wordlist', 
					help='contains the words we\'ll test', 
					metavar="FILE", 
					type=lambda x: is_valid_file(parser, x), required=True)
parser.add_argument('-s', '--success', 
					dest='success', 
					help='specifies the content that will be compared agains the server response to find vhosts', 
					type=nullable_string, required=False)
parser.add_argument('-f', '--failure', 
					dest='failure', 
					help='specifies the content that will be compared agains the server response to discard vhosts', 
					type=nullable_string, required=False)
parser.add_argument('-o', '--output-file', 
					dest='out_file', 
					help='the script can write all vhosts to this file', 
					metavar='FILE', 
					type=nullable_string, required=False)
args = parser.parse_args()

if args.success is None and args.failure is None:
	parser.error('Please specify either success (-s/--success) or failure (-f/--failure) content')

# opens and reads wordlist
f = open(args.wordlist, "r")
words = f.read().split("\n")

# setup toolbar
print('Brute-force in progress ...')

for word in words:
	vhost = word + '.' + args.domain
	req = "curl -H \'Host: " + vhost + "\' " + args.ip + " --silent"
	res = os.popen(req).read()

	# user specified success page content
	if args.success is not None and args.success in res:
		found_vhost(vhost, args.out_file)

	# user specified success page content
	if args.failure is not None and args.failure not in res:
		found_vhost(vhost, args.out_file)
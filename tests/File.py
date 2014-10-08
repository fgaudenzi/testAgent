#!/usr/bin/env python
import sys
import string
import json
import ConfigParser, getopt
from time import sleep
from patlib import convertChmodToBinary
from tests import Tester

def usage():
	print """\033[1m\033[91mCheck file permissions\033[0m\033[0m
	Usage: %s <input> <output>""" % __file__[__file__.rfind('/')+1:]

if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:i:o", ["host=","init=","output=","help"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for o, a in opts:
		if o in ("-h", "--host"):
			host = a
		elif o in  ("-o","--output"):
			output_folder = a+".log"
		elif o in  ("-i","--init"):
			config_file = a
		else:
			assert False, "unhandled option"


	config = config_file


	parser =  ConfigParser.RawConfigParser(allow_no_value=True)
	with open(config, 'r') as g:
		parser.readfp(g)





	host			=	parser.get("0","host")
	port 			=	int(parser.get("0","port")) or 22
	if parser.has_option("0","ssh_key_path"):
		ssh_key_path	=	parser.get("0","ssh_key_path")
	else:
		ssh_key_path	=	"~/.ssh/id_rsa"

	ssh_server_key_path	 =	parser.get("0","ssh_server_key_path")


	filepath		=	parser.get("1","filepath")
	chmod			=	parser.get("1","chmod")
	chmod_owner, chmod_group, chmod_other = convertChmodToBinary(chmod)
	username_owner	=	parser.get("2","username_owner")

	tester = Tester(host,username_owner,ssh_key_path,ssh_server_key_path,filepath,chmod,port) #REVIEW del prototipo
	
	print "[CHECKING CHMOD]"
	if tester.checkChmod() == True:
		print "success"
	else:
		print "failed"
		sys.exit(1)

	print "[TESTING OWNER READ]"
	if tester.checkRead((chmod_owner)[0]) == True:
		print "success"
	else:
		print "failed"
	print "[TESTING OWNER WRITE]"
	if tester.checkWrite((chmod_owner)[1]) == True:
		print "success"
	else:
		print "failed"


	username_group	=	parser.get("3","username_group")
	tester = Tester(host,username_group,ssh_key_path,ssh_server_key_path,filepath,chmod,port) #REVIEW del prototipo
	
	print "[TESTING GROUP READ]"
	sleep(1)
	if tester.checkRead((chmod_group)[0]) == True:
		print "success"
	else:
		print "failed"

	print "[TESTING GROUP WRITE]"
	sleep(1)
	if tester.checkWrite((chmod_group)[1]) == True:
		print "TESTING GROUP: write check success"
	else:
		print "TESTING GROUP: write check failed"

	username_other	=	parser.get("4","username_other")
	tester = Tester(host,username_other,ssh_key_path,ssh_server_key_path,filepath,chmod,port) #REVIEW del prototipo
	
	print "[TESTING OTHER READ]"
	sleep(1)
	if tester.checkRead((chmod_other)[0]) == True:
		print "TESTING OTHER: read check success"
	else:
		print "TESTING OTHER: read check failed"

	print "[TESTING OTHER WRITE]"
	sleep(1)
	if tester.checkWrite((chmod_other)[1]) == True:
		print "TESTING OTHER: write check success"
	else:
		print "TESTING OTHER: write check failed"




		

	
	

#!/usr/bin/env python
'''
@author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
'''


import sys
import string
import json
import ConfigParser, getopt
from time import sleep
from patlib import SSHClient
from patlib import DjangoDecryptor
from welighttests import Tester

def usage():
	print """\033[1m\033[91mCheck file permissions\033[0m\033[0m
	Usage: %s <input> <output>""" % __file__[__file__.rfind('/')+1:]

def exit_from_test():
	sys.exit(1)

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

	tester = Tester()
	mysql = False
	ssh = False
	try:
		##################################################
		#                                                #
		# STEP 0: LOADS WELIGHT HTTP URL                 #
		#                                                #
		##################################################

		step0_welighturl = """%s://%s:%s/""" % (parser.get("0","protocol"), parser.get("0","welighturl"), parser.get("0","welightport"),)
		step0_loginurl = step0_welighturl + "accounts/login/"

		##################################################
		#                                                #
		# STEP 1: LOGIN TO WELIGHT INTERFACE             #
		#                                                #
		##################################################

		step1_session = tester.loginAndGetCookies(step0_welighturl,step0_loginurl,parser.get("1","username"), parser.get("1","password"))

		##################################################
		#                                                #
		# STEP 2: GRAB VALUES FROM EDIT PAGE             #
		#                                                #
		##################################################
		try:
			step2_id = parser.get("2","id")
			step2_url = step0_welighturl  + "panels/admin/edit/" + step2_id
			step2_ip, step2_pwd = tester.getInputValues(step1_session,step2_url,['id_ip','id_password'])
		except:
			print "False2"
			exit_from_test()
		##################################################
		#                                                #
		# STEP 3: CONNECTS TO THE WELIGHT SERVER VIA SSH #
		#                                                #
		##################################################

		step3_username				= parser.get("3","username")
		step3_host					= parser.get("3","host")
		step3_port					= int(parser.get("3","port"))
		step3_ssh_key_path 			= parser.get("3","ssh_key_path")
		step3_ssh_server_key_path 	= parser.get("3","ssh_server_key_path")
		step3_welight_keyfile		= parser.get("3","welight_keyfile")
		step3_welight_metafile		= parser.get("3","welight_metafile")
		try:
			ssh = SSHClient(
				step3_host,
				step3_username,
				step3_ssh_key_path,
				step3_ssh_server_key_path,
				step3_port
				).connect()
			step3_welight_key  = ssh.executeCommand("cat " + step3_welight_keyfile)
			step3_welight_meta = ssh.executeCommand("cat " + step3_welight_metafile)
		except:
			print "False3"
			exit_from_test()
		##################################################
		#                                                #
		# STEP 4: BUILD SSH TUNNEL FOR MYSQL CONNECTION  #
		#                                                #
		##################################################

		step4_mysql_port			= int(parser.get("4","port"))
		step4_mysql_host			= parser.get("4","host")
		step4_mysql_local_port		= int(parser.get("4","local_port"))
		
		try:
			ssh.forwardPort(step4_mysql_local_port,step4_mysql_port,step4_mysql_host)
		except:
			print "False4"
			ssh.close()
			ssh = False
			exit_from_test()
		##################################################
		#                                                #
		# STEP 5: CONNECTS TO MYSQL                      #
		#                                                #
		##################################################

		step5_username			= parser.get("5","username")
		step5_password			= parser.get("5","password")
		step5_database			= parser.get("5","database")

		try:
			mysql = tester.mysqlConnect("127.0.0.1",step4_mysql_local_port,step5_username,step5_password,step5_database)
		except:
			print "False5"
			if ssh:
				ssh.close()
				ssh = False
			exit_from_test()
		##################################################
		#                                                #
		# STEP 6: GRAB THE VALUES FROM MYSQL             #
		#                                                #
		##################################################
		step6_table  			= parser.get("6","table")
		try:
			step6_ip, step6_pwd = tester.mysqlGetFields(mysql,step6_table,"id",step2_id,["ip","password"])
		except:
			print "False6"
			mysql.close()
			mysql = False
			if ssh:
				ssh.close()
				ssh = False
			exit_from_test()

		step6_ip = step6_ip[0]
		step6_pwd = step6_pwd[0]

		if mysql:
			mysql.close()
			mysql = False
		if ssh:
			ssh.close()
			ssh = False

		###################################################
		#                                                 #
		# STEP 7: CHECK ENCRYPTION - THEN DECRYPTS        #
		#                                                 #
		###################################################
		step7_encrypted_prefix = parser.get("7","encrypted_prefix")
		if step6_ip and step6_pwd:
			if step6_ip.startswith(step7_encrypted_prefix) and step6_pwd.startswith(step7_encrypted_prefix):
				step6_ip_decrypted, step6_pwd_decrypted = DjangoDecryptor().decrypt(step3_welight_meta,step3_welight_key,step6_ip[len(step7_encrypted_prefix):]), DjangoDecryptor().decrypt(step3_welight_meta,step3_welight_key,step6_pwd[len(step7_encrypted_prefix):])
				if step6_ip_decrypted == step2_ip and step6_pwd_decrypted == step2_pwd:
					print "True"
				else:
					print "False71"
					sys.exit(1)
			else:
				print "False72"
				sys.exit(1)
		else:
			print "False73"
			sys.exit(1)

		#STEP 8; COMPARE STEP5 VALUE TO STEP1

	except Exception as e:
		if mysql:
			mysql.close()
		if ssh:
			ssh.close()
		exit_from_test()
		raise
		
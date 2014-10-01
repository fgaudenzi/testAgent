#!/usr/bin/env python
import os
import sys
import getopt
import ConfigParser
import io
import subprocess
import logging

def usage():
    print "ehealthclient.py -p [port] -h [host]"



try:     
	opts, args = getopt.getopt(sys.argv[1:], "h:i:o:", ["host=","init=","output=","help"]) 
except getopt.GetoptError:           
        usage()                          
        sys.exit(2)  

for o, a in opts:
		if o in ("-h", "--host"):
			host=a
		elif o in  ("-o","--output"):
			output_folder = a+".log"
		elif o in  ("-i","--init"):
			config_file = a
		else:
			assert False, "unhandled option"


sample_config=config_file
#print sample_config
parser =  ConfigParser.RawConfigParser()
with open(sample_config, 'r') as g:
	parser.readfp(g)


try:
# adminlogin
	admin=parser.get("1", "admin")		
	adminpassword=parser.get("1", "password")		
	pathexecutor = "java -jar /Users/iridium/Jobs/ehealth-client-http.jar login "+admin+" "+adminpassword
	proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	list_output=out.split("\n")
	# list_output example ['1000071', 'User authenticated succesfully', '', '']
	checker=int(list_output[0])
	with open(output_folder, "a") as myfile:
		myfile.write(out+" \n")
	
	#print pathexecutor
	#print list_output
	
	
	if list_output[1]!="User authenticated succesfully" or checker<=0 :
		print "fail - admin login"
		sys.exit(-1)
	else:
		admin_id=list_output[0]




#create user
	username=parser.get("2", "username")			
	password=parser.get("2", "password")
	pathexecutor= "java -jar /Users/iridium/Jobs/ehealth-client-http.jar createuser "+username+" "+password+" "+admin_id
	proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	list_output=out.split("\n")
	
	checker=long(list_output[0])
	
	with open(output_folder, "a") as myfile:
		myfile.write(out +"\n")
	#print pathexecutor
	#print list_output
	
	if list_output[1]!="User registered succesfully" or checker<=0 :
		print "fail - user creation"+ list_output[1] 
		sys.exit(-2)
	else:
		user_id=list_output[0]

	# list_output example ['1000096', 'User registered succesfully', '', '']




#login user
	username=parser.get("3", "username")			
	wrongpassword=parser.get("3", "password")
	pathexecutor="java -jar /Users/iridium/Jobs/ehealth-client-http.jar login "+username+" "+wrongpassword
	proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	list_output=out.split("\n")
	checker=int(list_output[0])
	with open(output_folder, "a") as myfile:
		myfile.write(out +"\n")
	
	#print pathexecutor
	#print list_output
	
	if list_output[1]=="User locked - contact with administrator" and checker==-10:
		print "lockout - 1"
		sys.exit(0)
	elif list_output[1]!="invalid passowrd" and checker!=-11 :
		print "fail - user login succeed" 
		sys.exit(-2)
	# list_output example ['-11', 'Invalid password', '', '']


#login user
	username=parser.get("4", "username")			
	wrongpassword=parser.get("4", "password")
	pathexecutor="java -jar /Users/iridium/Jobs/ehealth-client-http.jar login "+username+" "+wrongpassword
	proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	list_output=out.split("\n")
	checker=int(list_output[0])
	with open(output_folder, "a") as myfile:
		myfile.write(out +"\n")
	
	#print pathexecutor
	#print list_output
	
	
	
	if list_output[1]=="User locked - contact with administrator" and checker==-10:
		print "lockout - 2"
		sys.exit(0)
	elif list_output[1]!="invalid passowrd" and checker!=-11 :
		print "fail - user login succeed" 
		sys.exit(-2)
#login user
	username=parser.get("5", "username")			
	wrongpassword=parser.get("5", "password")
	pathexecutor="java -jar /Users/iridium/Jobs/ehealth-client-http.jar login "+username+" "+wrongpassword
	proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	list_output=out.split("\n")
	checker=int(list_output[0])
	with open(output_folder, "a") as myfile:
		myfile.write(out +"\n")
	
	#print pathexecutor
	#print list_output
	
	
	
	

	if list_output[1]=="User locked - contact with administrator" and checker==-10:
		print "lockout - 3"
		sys.exit(0)
	elif list_output[1]!="invalid passowrd" and checker!=-11 :
		print "fail - user login succeed" 
		sys.exit(-2)
#login user
	username=parser.get("6", "username")			
	wrongpassword=parser.get("6", "password")
	pathexecutor="java -jar /Users/iridium/Jobs/ehealth-client-http.jar login "+username+" "+wrongpassword
	proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	list_output=out.split("\n")
	checker=int(list_output[0])
	
	with open(output_folder, "a") as myfile:
		myfile.write(out +"\n")
	
	#print pathexecutor
	#print list_output
	
	
	
	if list_output[1]=="User locked - contact with administrator" and checker==-10:
		print "lockout - 4"
		sys.exit(0)
	elif list_output[1]!="invalid passowrd" and checker!=-11 :
		print "fail - user login succeed" 
		sys.exit(-2)
#login user
	username=parser.get("7", "username")			
	wrongpassword=parser.get("7", "password")
	pathexecutor="java -jar /Users/iridium/Jobs/ehealth-client-http.jar login "+username+" "+wrongpassword
	proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	list_output=out.split("\n")
	checker=int(list_output[0])
	
	with open(output_folder, "a") as myfile:
		myfile.write(out +"\n")
	
	
	#print pathexecutor
	#print list_output
	
	
	
	if list_output[1]=="User locked - contact with administrator" and checker==-10:
		succeed=True
	elif list_output[1]!="invalid passowrd" and checker!=-11 :
		print "fail - user login succeed" 
		sys.exit(-2)

#check lockout
	pathexecutor="java -jar /Users/iridium/Jobs/ehealth-client-http.jar lockout "+username
	proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	list_output=out.split("\n")
	checker=int(list_output[0])
	
	#print pathexecutor
	#print list_output
	
	with open(output_folder, "a") as myfile:
		myfile.write(out +"\n")
	
	if list_output[1]=="Operation executed succesfully - user with id '"+user_id+"' locked? true" and checker==-10:
		succeed=True
	else:
		succeed=False

#delete user
	
	pathexecutor="java -jar /Users/iridium/Jobs/ehealth-client-http.jar deleteuser "+user_id
	proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
	#print pathexecutor
	(out, err) = proc.communicate()
	list_output=out.split("\n")
	with open(output_folder, "a") as myfile:
		myfile.write(out +"\n")


	if succeed==True:
		print "5"	
	else:
		print "fail - lockout unknonw"
	
	
except NameError,erro:
	with open(output_folder, "a") as myfile:
		myfile.write(out +"\n")
	print erro
	print sys.exc_info()[0]
	print "fail - value not found"

	sys.exit(2)

#os.system("java -jar /Users/iridium/Jobs/ehealth-client.jar login "+admin+" "+adminpassword+" >"+output_file)
# file = open(output_file, 'r')
# outputs=file.readlines()
# for line in outputs:
#	if line!="\n":
#		print line

# file.close()

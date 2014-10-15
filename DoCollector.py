#!/usr/bin/python
import subprocess
import ConfigParser
import os
import io
import sys
import logging

from xml.dom.minidom import parseString

class DoCollector:
	def __init__(self,inputa, executor, folder, repository):
		self.input=inputa
		self.executor=executor
		self.folder=folder
		self.repository=repository
		self.evidence=[]
		LOG_FILENAME = 'log-agent.log'
		self.agentLogger = logging.getLogger(LOG_FILENAME)
		self.agentLogger.info('Collector Init rep:'+repository+' - folder:'+folder+' - executor:'+executor+" - input:"+self.input)
		
		
 	
 	def starttest(self):
		if not os.path.exists(self.folder):
			os.makedirs(self.folder)
		pathexecutor=self.findexec()
		if pathexecutor==False:
			print "not found"
			sys.exit(-3)  
		
#		pathexecutor="/Users/iridium/Jobs/pythontAgents/ehealth.py"
		input=self.parserinput() 
#		create init file
#		config = ConfigParser.RawConfigParser()
		i=0
		for testcase in input:
			id_testcase=testcase[0]
			config_test=self.folder+'/config-'+id_testcase+'.ini'	
			output_test=self.folder+"/evidence-"+id_testcase+".out"
			self.evidence.append(output_test)
			#print "EVIDENCE:"+output_test
			config = ConfigParser.RawConfigParser()
			for singlelist in testcase[1:]:
				section=singlelist[0]
				config.add_section(section[(section.rfind("=")+1):])
				for single in singlelist[1:]:
					stop=single.rfind("=");
					config.set(section[(section.rfind("=")+1):],single[:stop],single[(stop+1):])
			
			
			with open(config_test, 'wb') as configfile:
				config.write(configfile)
			
			pathexecutor+=" --init="+config_test+" --output="+output_test
			self.agentLogger.info("Execution TestCase:"+id_testcase+" -command: python "+pathexecutor)
			proc = subprocess.Popen(["python "+pathexecutor], stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()
			print "OUTPUT TEST:"+out
			with open(output_test, "w") as f:
				f.write(out)


#		proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
#		(out, err) = proc.communicate()
#		return result

#		create output file
#		locate from repository script
#		exec python script
#		
	def findexec(self):
		from os import listdir
		from os.path import isfile
		lista=[]
		mypath=self.repository
		#print mypath+"/"+self.executor
		#print listdir(mypath)
		for f in listdir(mypath):
			if isfile(mypath+"/"+f):
				lista=lista+[f]
		print lista
		print self.executor
		if self.executor in lista:
			return mypath+"/"+self.executor
		return False	
			
	def parserinput(self):
		from xml.dom.minidom import parseString
		data=self.input
		dom1 = parseString(data)
		dom=dom1.getElementsByTagName("TestCase")
		len_xml=dom.length
		testcase=[];
		for i in range(0,len_xml):
			elems=dom.item(i).getElementsByTagName('TestInstance')
			tc_id=dom.item(i).getElementsByTagName('ID')
			tc_id=[tc_id[0].childNodes[0].nodeValue]
			listainput=[]
			for elem in elems:
					templateid="testintance="+elem.getAttribute("Operation")
					inputelements=elem.getElementsByTagName('Input')
					if len(inputelements[0].childNodes)>0:
						inputelem=inputelements[0].childNodes[0].nodeValue+" "
						inputs=inputelem.split()
						inputs=[templateid]+inputs
						listainput+=[inputs]
			testcase.append(tc_id+listainput)
		return testcase
		#for tc in testcase:
		#	print tc[0]
		#	for testinstance in tc[1:]:
		#		print testinstance
#  		xmlTag = dom.getElementsByTagName('Input')[0].nodevalue
#  		print xmlTag
	def getEvidences(self):
		result=""
		for ev in self.evidence:
			ev_codes=ev.split('/')
			ev_code=ev_codes[len(ev_codes)-1]
			with open(ev,'r') as f:
				#result=result+ev_code+"$"+f.read()+"\n"
				result=result+f.read()+"\n"
		return result
			
	
	

#inputdata="<TestCases><TestCase><ID>1</ID><Description>TestCase1</Description><TestInstance Operation=\"1\"><Preconditions/><HiddenCommunications/><Input>admin=admin password=admin1</Input><ExpectedOutput>true</ExpectedOutput><PostConditions/></TestInstance><TestInstance Operation=\"2\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=pass1234</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"3\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=xxx</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"4\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=1234pass</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"5\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=password</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"6\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=usertest</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"7\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=testpwd</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"8\"><Preconditions>user-id</Preconditions><HiddenCommunications/><Input>lockout=true</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance></TestCase><TestCase><ID>1</ID><Description>TestCase1</Description><TestInstance Operation=\"1\"><Preconditions/><HiddenCommunications/><Input>admin=admin password=admin1</Input><ExpectedOutput>true</ExpectedOutput><PostConditions/></TestInstance><TestInstance Operation=\"2\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=pass1234</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"3\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=xxx</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"4\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=1234pass</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"5\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=password</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"6\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=usertest</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"7\"><Preconditions>admin-id</Preconditions><HiddenCommunications/><Input>username=usertest password=testpwd</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"8\"><Preconditions>user-id</Preconditions><HiddenCommunications/><Input>lockout=true</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance></TestCase></TestCases>"		
#inputdata="<TestCases><TestCase><ID>1</ID><Description>TestCase1</Description><TestInstance Operation=\"1\"><Preconditions></Preconditions><HiddenCommunications></HiddenCommunications><Input>admin=admin password=admin1</Input><ExpectedOutput>true</ExpectedOutput><PostConditions></PostConditions></TestInstance><TestInstance Operation=\"2\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=pass1234</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"3\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=xxx</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"4\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=1234pass</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"5\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=password</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"6\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=usertest</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"7\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=testpwd</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"8\"><Preconditions>user-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>lockout=true</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance></TestCase><TestCase><ID>22</ID><Description>TestCase1</Description><TestInstance Operation=\"1\"><Preconditions></Preconditions><HiddenCommunications></HiddenCommunications><Input>admin=admin password=admin1</Input><ExpectedOutput>true</ExpectedOutput><PostConditions></PostConditions></TestInstance><TestInstance Operation=\"2\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=pass1234</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"3\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=xxx</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"4\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=1234pass</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"5\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=password</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance></TestCase></TestCases>"
#oggetto=DoCollector(inputdata,"ehealth.py","/Users/iridium/Jobs/pythonAgents/newF","/Users/iridium/Jobs/pythonAgents")
#oggetto.parserinput()
#oggetto.starttest()

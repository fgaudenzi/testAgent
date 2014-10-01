#!/usr/bin/python
import ConfigParser
import os
from DoCollector import DoCollector
import pika
from xml.dom.minidom import parseString
from toManagerRabbitSender import ManagerNotifier
from threading import Thread
import logging

def doCollection(cm_id,collector,messanger):
	print "Test STARTING"
	collector[1].starttest()
	print "Test DONE"
	print collector[1].getEvidences();
	mess=collector[1].getEvidences();
	messanger.sendMessage(cm_id,collector[0],mess)
		



class DoCertify:
	def __init__(self,xml_message,notifier):
		
		self.notifier=notifier
		self.xml_message=xml_message
		dom = parseString(self.xml_message)
		cm=dom.getElementsByTagName('cm')
		self.cm_id=cm[0].getAttribute('id')
		LOG_FILENAME = 'DoCertify'
		self.agentLogger = logging.getLogger(LOG_FILENAME)
		self.agentLogger.info('Certificate Init CM_ID:'+self.cm_id);
	

	def startCertification(self):
		
		from os.path import expanduser
		home = expanduser("~")
		sample_config=home+"/.agent/agent.ini"
		parser =  ConfigParser.RawConfigParser()
		with open(sample_config, 'r') as g:
			parser.readfp(g)
		dep_folder=parser.get("all","deployment")+"/"+self.cm_id
		rep_folder=parser.get("all","repository")
		#if not os.path.exists(dep_folder):
		#	os.makedirs(dep_folder)
			
		dom = parseString(self.xml_message)
		elems=dom.getElementsByTagName('collector')	
		colls=[]
		for collector in elems:
			collector_id=collector.getAttribute('id')	
			#get TestCases			
			testCases=collector.getElementsByTagName('TestCases').item(0).toxml()
			tot=collector.getAttribute("tot")
			app_coll=DoCollector(testCases,tot,dep_folder+"/"+collector_id,rep_folder)
			colls.append([collector_id,app_coll])
		
		self.threads = []

		for collector in colls:
			self.agentLogger.info('CM:'+self.cm_id+'-COL:'+collector_id+' - Starting Collector')
			t = Thread(target=doCollection, args=(self.cm_id,collector,self.notifier))
			t.start()
			self.threads.append(t)
		
		
		
		
#		for collector in colls:
#			collector[1].starttest()
#			messagge=collector[1].getEvidences();
#			self.notifier.sendMessage(collector[0],message)

			
	
			
	def collectorend(self):
		self.connection.close()
		

	
#xml_message="<cm id=\"cm24\"><collector id=\"coll1\" tot=\"ehealth.py\"><TestCases><TestCase><ID>1</ID><Description>TestCase1</Description><TestInstance Operation=\"1\"><Preconditions></Preconditions><HiddenCommunications></HiddenCommunications><Input>admin=admin password=admin1</Input><ExpectedOutput>true</ExpectedOutput><PostConditions></PostConditions></TestInstance><TestInstance Operation=\"2\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=pass1234</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"3\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=xxx</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"4\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=1234pass</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"5\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=password</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"6\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=usertest</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"7\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=testpwd</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"8\"><Preconditions>user-id</Preconditions><HiddenCommunications></HiddenCommunications><Input></Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance></TestCase><TestCases><TestCase><ID>25</ID><Description>TestCase1</Description><TestInstance Operation=\"1\"><Preconditions></Preconditions><HiddenCommunications></HiddenCommunications><Input>admin=admin password=admin1</Input><ExpectedOutput>true</ExpectedOutput><PostConditions></PostConditions></TestInstance><TestInstance Operation=\"2\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=pass1234</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"3\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=xxx</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"4\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=1234pass</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"5\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=password</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"6\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=usertest</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"7\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=testpwd</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"8\"><Preconditions>user-id</Preconditions><HiddenCommunications></HiddenCommunications><Input></Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance></TestCase></TestCases></collector></cm>"
#xml_message="<cm id=\"cm24\"><collector id=\"coll1\" tot=\"ehealth.py\"><TestCases><TestCase><ID>1</ID><Description>TestCase1</Description><TestInstance Operation=\"1\"><Preconditions></Preconditions><HiddenCommunications></HiddenCommunications><Input>admin=admin password=admin1</Input><ExpectedOutput>true</ExpectedOutput><PostConditions></PostConditions></TestInstance><TestInstance Operation=\"2\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=pass1234</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"3\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=xxx</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"4\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=1234pass</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"5\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=password</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"6\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=usertest</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"7\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=testpwd</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"8\"><Preconditions>user-id</Preconditions><HiddenCommunications></HiddenCommunications><Input></Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance></TestCase><TestCase><ID>25</ID><Description>TestCase1</Description><TestInstance Operation=\"1\"><Preconditions></Preconditions><HiddenCommunications></HiddenCommunications><Input>admin=admin password=admin1</Input><ExpectedOutput>true</ExpectedOutput><PostConditions></PostConditions></TestInstance><TestInstance Operation=\"2\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=pass1234</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"3\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=xxx</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"4\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=1234pass</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"5\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=password</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"6\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=usertest</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"7\"><Preconditions>admin-id</Preconditions><HiddenCommunications></HiddenCommunications><Input>username=usertest password=testpwd</Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance><TestInstance Operation=\"8\"><Preconditions>user-id</Preconditions><HiddenCommunications></HiddenCommunications><Input></Input> <ExpectedOutput>login</ExpectedOutput><PostConditions>true</PostConditions></TestInstance></TestCase></TestCases></collector></cm>"
#senders=ManagerNotifier("agent1")
#cert=DoCertify(xml_message,senders)
#cert.startCertification()
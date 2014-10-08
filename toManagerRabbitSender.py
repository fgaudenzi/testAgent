#!/usr/bin/python
import pika
import socket
import ssl

class ManagerNotifier:
	def __init__(self,agent_id):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# require a certificate from the server
		dic= {'certfile': "/opt/testAgent/certificates/client/cert.pem", 'keyfile': "/opt/testAgent/certificates/client/key.pem"}
		credentials= pika.credentials.PlainCredentials('user1','pass1')
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',virtual_host ='vTestManager',credentials=credentials,ssl=True,ssl_options=dic,port=5671))
#sender=ManagerNotifier(connection,"agent1")
#sender.sendMessage("CIAO")
		self.connection=connection
		self.channel = self.connection.channel()
		self.severity="key-test"
		self.agent_id=agent_id
		self.channel.exchange_declare(exchange='collector_agents',type='direct')
        
        
	def sendMessage(self,cm_id,collector,message):
		print
		print "SENDING"
		print message	
		message=self.agent_id+"#"+cm_id+"#"+collector+"#"+message	
		self.channel.basic_publish(exchange='collector_agents',routing_key=self.severity,body=message)
                      
	def closeConnection(self):
		self.connection.close()    	
		
		
#no=ManagerNotifier("agent1")
#no.sendMessage("CIAO BELLI")
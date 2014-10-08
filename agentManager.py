#!/usr/bin/env python

import sys
import daemon
import socket
import ssl
import urllib
import time
import pika
from toManagerRabbitSender import ManagerNotifier
from DoCertify import DoCertify
import logging


def callback(ch, method, properties, body):
	#print " [x] %r" % (body,)
	LOG_FILENAME = 'receiver'
	agentLogger = logging.getLogger(LOG_FILENAME)
	agentLogger.info('Received message with body:\n'+body)
	certification_model=DoCertify(body,sender)
	certification_model.startCertification();


def do_something():
	LOG_FILENAME = 'log-agent.log'
	logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.INFO,
                    )

	agentLogger = logging.getLogger("AgentManager")
	agentLogger.info('Agent Started and listening')
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# require a certificate from the server
	'''ssl_sock = ssl.wrap_socket(
		s,server_side=True,
		ca_certs="/etc/ssl/certs/ca-bundle.crt",
		certfile="/opt/testAgent/certificates/client/cert.pem",
		keyfile="/opt/testAgent/certificates/client/key.pem"
		)'''
	
	dic = {
	'certfile': "/opt/testAgent/certificates/client/cert.pem",
	'keyfile': "/opt/testAgent/certificates/client/key.pem",
	'ca_certs':"/opt/testAgent/certificates/testca/cacert.pem",
	
	}

	credentials= pika.credentials.PlainCredentials('user1','pass1')
	global sender
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(
			host='localhost',
			virtual_host ='vTestManager',
			credentials=credentials,
			ssl=True,
			ssl_options=dic,
			port=5671
			)
		)
	sender=ManagerNotifier("agent1")
	channel = connection.channel()
	channel.exchange_declare(exchange='broadcast_to_agent',
								type='fanout')
	result = channel.queue_declare(exclusive=True)
	queue_name = result.method.queue

	channel.queue_bind(exchange='broadcast_to_agent',
								queue=queue_name)
		
	print ' [*] Waiting for logs. To exit press CTRL+C'
	channel.basic_consume(callback,queue=queue_name,no_ack=True)
	channel.start_consuming()	

# 	while True:			
	connection.close()
	

def run():
    #with daemon.DaemonContext():
    do_something()







run()

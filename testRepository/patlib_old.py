import socket,paramiko

class SSHClient(object):
	def __init__(self,hostname,username,keyfile,serverkeyfile,port=22):
		self.hostname = hostname
		self.ip = socket.gethostbyname(hostname)
		self.username = username
		self.keyfile = keyfile
		self.port = port
		self.connected = False
		self.client = paramiko.SSHClient()
		self.client.load_host_keys(serverkeyfile)
		#self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	def connect(self):
		self.client.connect(self.hostname, self.port, self.username, key_filename=self.keyfile)
		self.connected = True

	def executeCommand(self,command=""):
		if (self.connected == False):
			raise Exception, "Not connected"
		if (command==""):
			raise Exception, "No command"
		stdin,stdout,stderr = self.client.exec_command(command)
		out = stdout.readlines()
		output=""
		for line in out:
			if line != '':
				output=output+line
		return output

	def close(self):
		self.client.close()



def convertChmodToBinary(chmod):
	chmod = str(chmod)
	a = [['0','0','0'],['0','0','0'],['0','0','0']]
	for i in range(0,3):
		digit = int(chmod[i])
		for j in range(0,3):
			a[i][j] = str(int(digit/pow(2,2-j)) % 2)
	return a
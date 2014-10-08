from patlib import SSHClient

class Tester(object):
	def __init__(self,hostname,username,keyfile,serverkeyfile,filename,chmod,port=22):
		self.hostname = hostname
		self.username = username
		self.keyfile = keyfile
		self.serverkeyfile = serverkeyfile
		self.port = port
		self.filename = filename
		self.chmod = chmod

	def checkChmod(self):
		ssh = SSHClient(self.hostname,self.username,self.keyfile,self.serverkeyfile,self.port)
		ssh.connect()
		filelist = ssh.executeCommand("stat -c \"%a\" " + self.filename)
		for eachFile in filelist.split("\n"):
			if eachFile and eachFile != self.chmod:
				ssh.close()
				return False
		ssh.close()
		return True


	def checkRead(self,hasToBe):
		ssh = SSHClient(self.hostname,self.username,self.keyfile,self.serverkeyfile,self.port)
		ssh.connect()
		filelist = ssh.executeCommand("stat  -c \"%n\" " + self.filename)
		filelistsplitted = filelist.split("\n")
		for eachFile in filelistsplitted[0:len(filelistsplitted)-1]:
			command = 'echo -e "try:\\n\\topen(\\"' + eachFile + '\\",\\"r\\");\\n\\tprint(\\"True\\")\\nexcept IOError:\\n\\tprint(\\"False\\")" | python'
			print "----"
			print "Executing " + command
			output = ssh.executeCommand(command)
			output = output.strip("\n")
			print "Got " + output
			print "Had to be " + hasToBe
			if (hasToBe == '1' and output == 'False') or (hasToBe == '0' and output == 'True'):
				ssh.close()
				return False
		ssh.close()
		return True

	def checkWrite(self,hasToBe):
		ssh = SSHClient(self.hostname,self.username,self.keyfile,self.serverkeyfile,self.port)
		ssh.connect()
		filelist = ssh.executeCommand("stat  -c \"%n\" " + self.filename)
		filelistsplitted = filelist.split("\n")
		for eachFile in filelistsplitted[0:len(filelistsplitted)-1]:
			command = 'echo -e "try:\\n\\topen(\\"' + eachFile + '\\",\\"w\\");\\n\\tprint(\\"True\\")\\nexcept IOError:\\n\\tprint(\\"False\\")" | python'
			print "----"
			print "Executing " + command
			output = ssh.executeCommand(command)
			output = output.strip("\n")
			print "Got " + output
			print "Had to be " + hasToBe
			if (hasToBe == '1' and output == 'False') or (hasToBe == '0' and output == 'True'):
				ssh.close()
				return False
		ssh.close()
		return True

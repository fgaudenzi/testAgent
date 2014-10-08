File.py
	Tests file confidentiality in file system.
	It checks the CHMODs to be equal to the ones defined in the input config file.
	Then it tries to access to the target file both in read and write modes, checking effectively that chmods are respected and not manipulated in some way.
	The input file describes a FSM that gets:
	
		[0]
		host=hostnameOfServer					#the hostname of the server to connect to through SSH
		port=22							#SSH port for the server above
		ssh_key_path=ssh_private_key				#SSH private key. The public key has to be on the server before launching the test
		ssh_server_key_path=ssh_public_key			#SSH public key of the server, to authenticate it

		[1]
		filepath=/file/to/verify				#absolute path  of the target file
		chmod=600						#chmods

		[2]
		username_owner=usernameOwner				#username of the owner

		[3]
		username_group=usernameGroup				#username of a user that is in the same unix group of the owner

		[4]
		username_other=usernameOther				#username of another user that isn't in the same unix group of the owner

	The third users specified above must have testAgent's ssh public key in their ~/.ssh/authorized_keys file
	
	NOT YET IMPLEMENTED: output file for logging (now everything is printed out to stdout). I will add a method to log in patlib.py



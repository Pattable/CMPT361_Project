import json
import socket
import os, glob, datetime
import sys
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad

def server():
	#Server port
	serverPort = 13000

	#Create server socket that uses IPv4 and TCP protocols 
	try:
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print('Error in server socket creation:',e)
		sys.exit(1)

	#Associate 13000 port number to the server socket
	try:
		serverSocket.bind(('', serverPort))
	except socket.error as e:
		print('Error in server socket binding:',e)
		sys.exit(1)        

	print('The server is ready to accept connections')

	#The server can only have five connections in its queue waiting for acceptance
	serverSocket.listen(5)

	while 1:
		try:
			#Server accepts client connection
			connectionSocket, addr = serverSocket.accept()
			print(addr,'   ',connectionSocket)
			pid = os.fork()

			# If it is a client process
			if pid == 0:

				serverSocket.close()
				
				# Decrypt with server private key
				with open('server_private.pem', mode='rb') as file:
					private_key = file.read()
				
				privkey = RSA.import_key(private_key)
				cipher_rsa_dec = PKCS1_OAEP.new(privkey)
				
				# Split userpass string into username and password
				userpass = cipher_rsa_dec.decrypt(connectionSocket.recv(2048)).decode('ascii').split(',')
				
				with open('user_pass.json') as file:
					userpass_json = json.load(file)
				
				# Authenticate if client username and password in json
				auth = False
				for e in userpass_json:
					if userpass[0] == e and userpass[1] == userpass_json.get(e):
						connectionSocket.send('OK'.encode('ascii'))
						
						print('Connection Accepted and Symmetric Key Generated for client:', userpass[0])
						auth = True
						break
					
				if auth == False:
					connectionSocket.send('Invalid username or password'.encode('ascii'))
					
					print('The received client information:', userpass[0], 'is invalid (Connection Terminated).')
					connectionSocket.close()
					return
				
				# Generate Key
				KeyLen = 256
				sym_key = get_random_bytes(int(KeyLen/8))
				
				# Generate Cyphering Block
				cipher = AES.new(sym_key, AES.MODE_ECB)
				
				# Encrypt sym_key with client public key and send to client
				with open(userpass[0] + '_public.pem', mode='rb') as file:
					public_key = file.read()
				
				pubkey = RSA.import_key(public_key)
				cipher_rsa_en = PKCS1_OAEP.new(pubkey)
				
				# Encode then encrypt
				connectionSocket.send(cipher_rsa_en.encrypt(sym_key))
				
				# Decrypt then unpad then decode
				message = unpad(cipher.decrypt(connectionSocket.recv(2048)), 16).decode('ascii')
				
				# Send menu
				if message == 'OK':
					while 1:
						connectionSocket.send(cipher.encrypt(pad('Select the operation:\n		1) Create and send an email\n		2) Display the inbox list\n		3) Display the email contents\n		4) Terminate the connection\n\n		choice:		'.encode('ascii'), 16)))
					
						# Get choice from client
						message = unpad(cipher.decrypt(connectionSocket.recv(2048)), 16).decode('ascii')
						
						# Sending Email Subprotocol
						if message == '1':
							connectionSocket.send(cipher.encrypt(pad('Sending Email Subprotocol'.encode('ascii'), 16)))
						
						# Viewing Inbox Subprotocol
						elif message == '2':
							connectionSocket.send(cipher.encrypt(pad('Viewing Inbox Subprotocol'.encode('ascii'), 16)))
						
						# Viewing Email Subprotocol
						elif message == '3':
							connectionSocket.send(cipher.encrypt(pad('Viewing Email Subprotocol'.encode('ascii'), 16)))
						
						# Connection Termination Subprotocol
						elif message == '4':
							print('Terminating connection with', userpass[0])
							
							connectionSocket.close()
							return

			#Parent doesn't need this connection
			connectionSocket.close()

		except socket.error as e:
			print('An error occured:',e)
			serverSocket.close() 
			sys.exit(1)        
		except:
			print('Goodbye')
			serverSocket.close() 
			sys.exit(0)


#-------
server()

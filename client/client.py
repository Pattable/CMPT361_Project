import json
import socket
import os, glob, datetime
import sys
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad

def client():
	# Server Information
	serverName = input('Enter the server name or IP address: ')
	serverPort = 13000

	#Create client socket that useing IPv4 and TCP protocols 
	try:
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print('Error in client socket creation:',e)
		sys.exit(1)    

	try:
		#Client connect with the server
		clientSocket.connect((serverName,serverPort))
		
		# Ask for client username and password
		username = input('Enter your username: ')
		password = input('Enter your password: ')
		
		userpass = username + ',' + password
		
		# Encrypt with server public key and send to server
		with open('server_public.pem', mode='rb') as file:
			public_key = file.read()
		
		pubkey = RSA.import_key(public_key)
		cipher_rsa_en = PKCS1_OAEP.new(pubkey)
		
		clientSocket.send(cipher_rsa_en.encrypt(userpass.encode('ascii')))
		
		# Get server response to username and password
		message = clientSocket.recv(2048).decode('ascii')
		
		if message == 'OK':
		
			# Decrypt sym_key with client private key
			with open(username + '_private.pem', mode='rb') as file:
				private_key = file.read()
			
			privkey = RSA.import_key(private_key)
			cipher_rsa_dec = PKCS1_OAEP.new(privkey)
			
			# Decrypt then decode ascii
			sym_key = cipher_rsa_dec.decrypt(clientSocket.recv(2048))
			
			# Generate Cyphering Block
			cipher = AES.new(sym_key, AES.MODE_ECB)
			
			# Send OK encrypted with sym_key to server. Encode then pad then encrypt.
			clientSocket.send(cipher.encrypt(pad('OK'.encode('ascii'), 16)))
			
			while 1:
				# Get menu from server. Decrypt then unpad then decode.
				message = unpad(cipher.decrypt(clientSocket.recv(2048)), 16).decode('ascii')
				
				# Send choice to server
				num = ''
				while num == '':
					num = input(message)
				
				clientSocket.send(cipher.encrypt(pad(num.encode('ascii'), 16)))
				
				# Sending Email Subprotocol
				if num == '1':
					print(unpad(cipher.decrypt(clientSocket.recv(2048)), 16).decode('ascii'))
				
				# Viewing Inbox Subprotocol
				elif num == '2':
					print(unpad(cipher.decrypt(clientSocket.recv(2048)), 16).decode('ascii'))
				
				# Viewing Email Subprotocol
				elif num == '3':
					print(unpad(cipher.decrypt(clientSocket.recv(2048)), 16).decode('ascii'))
				
				# Connection Termination Subprotocol
				elif num == '4':
					print('The connection is terminated with the server.')
					break					
				
		else:
			# 'Invalid username or password'
			message += '.\nTerminating.'
			print(message)
		
		# Client terminate connection with the server
		clientSocket.close()

	except socket.error as e:
		print('An error occured:',e)
		clientSocket.close()
		sys.exit(1)

#----------
client()

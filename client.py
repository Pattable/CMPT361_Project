'''
Name: Patrick Huynh
ID: 3062065
Class: CMPT 361 AS01 X02L
'''

import socket
import os
import sys
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def client():
	# Server Information
	serverName = input('Enter the server name or IP address: ')
	serverPort = 12000

	#Create client socket that useing IPv4 and TCP protocols 
	try:
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print('Error in client socket creation:',e)
		sys.exit(1)    

	try:
		#Client connect with the server
		clientSocket.connect((serverName,serverPort))

		# Open key file
		with open('key', mode='rb') as file:
			key = file.read()

		# Generate Cyphering Block
		cipher = AES.new(key, AES.MODE_ECB)

		# Enter username
		message = unpad(cipher.decrypt(clientSocket.recv(2048)), 16).decode('ascii')

		# Client send username to the server
		message = input(message)
		clientSocket.send(cipher.encrypt(pad(message.encode('ascii'), 16)))

		while 1:
			for i in range(4):
				# Get question
				message = unpad(cipher.decrypt(clientSocket.recv(2048)), 16).decode('ascii')
				print(message)

				# Send answer
				message = input('Answer: ')
				clientSocket.send(cipher.encrypt(pad(message.encode('ascii'), 16)))

			# Get score, then 'Would you like to try again? (y/n)'
			message = unpad(cipher.decrypt(clientSocket.recv(2048)), 16).decode('ascii')

			# Send answer
			message = input(message)
			clientSocket.send(cipher.encrypt(pad(message.encode('ascii'), 16)))

			if message == 'y' or message == 'Y':
				continue
			else:
				break

		# Client terminate connection with the server
		clientSocket.close()

	except socket.error as e:
		print('An error occured:',e)
		clientSocket.close()
		sys.exit(1)

#----------
client()

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

def server():
	#Server port
	serverPort = 12000

	#Create server socket that uses IPv4 and TCP protocols 
	try:
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print('Error in server socket creation:',e)
		sys.exit(1)

	#Associate 12000 port number to the server socket
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

				# Open key file
				with open('key', mode='rb') as file:
					key = file.read()

				# Generate Cyphering Block
				cipher = AES.new(key, AES.MODE_ECB)

				#Server send welcome to the client
				connectionSocket.send(cipher.encrypt(pad('Welcome to examination System\n\nEnter your name: '.encode('ascii'), 16)))

				#Server receives client username
				encrypted_message = connectionSocket.recv(2048)
				print('Encrypted message received:', encrypted_message)

				user = str(unpad(cipher.decrypt(encrypted_message), 16).decode('ascii'))
				print('Decrypted message received:', user)
				
				# Math questions loop
				while True:
					count = 0
					
					# Do 4 times
					for i in range(1, 5):
						# Choose num1, num2, sign
						num1 = random.randint(0, 100)
						num2 = random.randint(0, 100)
						sign_choice = random.randint(0, 2)
						
						# Addition
						if sign_choice == 0:
							question = 'Question ' + str(i) + ': ' + str(num1) + ' + ' + str(num2) + ' ='
							answer = num1 + num2
						
						# Subtraction
						elif sign_choice == 1:
							question = 'Question ' + str(i) + ': ' + str(num1) + ' - ' + str(num2) + ' ='
							answer = num1 - num2
						
						# Multiplication
						else:
							question = 'Question ' + str(i) + ': ' + str(num1) + ' * ' + str(num2) + ' ='
							answer = num1 * num2

						# Send question to client
						connectionSocket.send(cipher.encrypt(pad(question.encode('ascii'), 16)))

						# Get answer from client
						encrypted_message = connectionSocket.recv(2048)
						print('Encrypted message received from', user + ':', encrypted_message)

						stud_ans = str(unpad(cipher.decrypt(encrypted_message), 16).decode('ascii'))
						print('Decrypted message received from', user + ':', stud_ans)

						# Check client answer
						try: 
							if int(stud_ans) == answer:
								count += 1
						except:
							pass

					total = 'You achieved a score of ' + str(count) + '/4\nWould you like to try again? (y/n)\n'
					connectionSocket.send(cipher.encrypt(pad(total.encode('ascii'), 16)))

					# Client answers 'Y' or 'N'
					encrypted_message = connectionSocket.recv(2048)
					print('Encrypted message received from', user + ':', encrypted_message)

					restart = str(unpad(cipher.decrypt(encrypted_message), 16).decode('ascii'))
					print('Decrypted message received from', user + ':', restart)

					if restart == 'y' or restart == 'Y':
						continue
					else:
						break

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

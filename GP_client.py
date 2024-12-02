# This is an example from "Computer Networking: A Top Down Approach" textbook chapter 2
import socket
import sys
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
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

        #2.1: Ask client user to enter email destination clients' 
        # username and email title
        from_user = input('From: ')
        to_user = input('To: ')
        title = input('Enter Title: ')
        terminal_or_txt = input("Mesage written on terminal or text file (terminal vs. txt))")

        if (terminal_or_txt == 'txt'): 
            filename = input('Enter filename: ')
            try:
                file = open(filename, "r")
            except:
                print("File error")
                return None
            lines = file.readlines()
            message = ''.join(lines)
            print(message)
            
        elif (terminal_or_txt == 'terminal'):
            message = input('Enter your message:')

        content_len = len(message)

        
        #send the message to the server(change later)
        combine_send = 'From: ' + from_user + '\nTo: ' + to_user + '\nTitle' + title + '\nContent Length: ' + str(content_len) + '\nContent:\n' + message

        #send combine_send to the server
        clientSocket.send(combine_send.encode('ascii'))

        # Client terminate connection with the server
        clientSocket.close()
        

    except socket.error as e:
        print('An error occured:',e)
        clientSocket.close()
        sys.exit(1)

#----------
client()

"""
Client created for 3357 Assignment 2
Author: Ben Dumais, 250669195
Please use Python 2.7
"""

"""
USAGE:
	enter a valid IP and Port when prompted. If a server is found with those details,
	client will prompt you for a query to send
	Once data is sent, it waits for a response and then displays it before exiting
	Only valid query is: What is the current date and time?
"""

import socket

#Debug variable, set to true to skip IP and Port input
debug = False

if debug == False:
    TCP_IP = raw_input("Please enter the IP of the server: " )	#Get IP from user
    TCP_PORT = int(raw_input("Please enter the Port: "))		#Get Port from user
else:
    TCP_IP = '192.168.14.1'
    TCP_PORT = 5005

#Create Socket from given info
print "Attempting to contact server at ",TCP_IP,":",TCP_PORT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Attempt to server
try:
    s.connect((TCP_IP, TCP_PORT))
    print ("Connection to Server Established")
except Exception as e:
	#If an error is thrown, input data is likely invalid so display error and exit
    print ("Error connecting to server, please enter valid IP and Port")
    s.close()
    quit()
	
query = raw_input("server> ") #Prompt user for a query	
s.send(query)					#Send to server through socket

result = s.recv(2048)	#Wait for a reply on the socket

print result			#Print the query's result

s.close()				#Close connection and exit
print("Connection Closed")
    
    

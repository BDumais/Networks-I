"""
Server created for 3357 Assignment 2
Author: Ben Dumais, 250669195
Please use Python 2.7
"""

"""
USAGE:
	enter a valid IP and Port when prompted. If successful, server
	will be created and begin listening for a connection
	Once a connection is received, the server will wait to receive data
	Once data is received, it fetches appropriate response and sends it back before closing
	Only valid query from client is: What is the current date and time?
	Returns date and time in MM/DD/YYY HH:MM:SS format
"""

import socket
import time

#Debug Variable, set to False to skip ip and port inputs
debug = False

if debug == False:
    TCP_IP = raw_input("Please enter the IP to use: " )	#Prompt for IP
    TCP_PORT = int(raw_input("Please enter a Port: "))	#Prompt for port and convert to int
else:
    TCP_IP = '192.168.14.1'	#Defaults
    TCP_PORT = 5005

#Try to setup a server with the input data
try:	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	print "Server listening on " + TCP_IP + ":",TCP_PORT
	
except Exception as e:	#If an exception is thrown, display error and exit
	print("Error attempting to create server, please enter valid IP and Port")
	s.close()	#Close connection
	quit()		#Quit

#Otherwise, wait for a connection
conn, addr = s.accept()
print "Connection to Client Established:", addr	#Display client info when received

#Wait to receive query
query = conn.recv(2048)
	
print ("Received query")	#Notify that a query has been received
	
#Check the query to see if it is valid	
if query == "What is the current date and time?":
	#If so, create string from current date and time
	result = "Current Date and Time - " + time.strftime('%m/%d/%Y %H:%M:%S')

else:	#Otherwise we send an error
	result = "Invalid query, please retry"
	
#Send result of query and close	
conn.send(result)
conn.close()
print("Server Closing")
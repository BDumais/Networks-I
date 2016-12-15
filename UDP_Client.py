"""
3357 Assignment 4, UDP_Client
Written by Ben Dumais (250669195)
"""

import binascii
import socket
import struct
import sys
import hashlib

"""## DEFINE METHODS ##"""

"""
Method to compute the checksum value of a packet
Takes ack number, sequence number, and data as parameters
"""
def computeCheckSum(a, s, d):
	data = (a,s,d)	#Data to be used in datagram
	UDP_Data = struct.Struct('I I 8s')	#Define structure of data
	packed_data = UDP_Data.pack(*data)	#Pack Data
	chksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8") #Calculate bytes
	return chksum	#Return value

"""
RDT Method, used to manage RDT functionality
This method handles all the logic and data comparison. Method terminates when
non corrupt data, proper data is received.
Takes data and sequence number as parameters
"""
def RDT(data, seq):

	RDTSend(seq, data)	#Send data via RDT procedure
	result = RDTWait()	#Get reply from Server
	
	if not result == "Timeout":	#If returned result is not the timedout string, continue

		chksum = computeCheckSum(result[0],result[1],result[2])	#Calculate the checksum of the reply
		
		if result[3] == chksum:	#If checksums match, compare sequence number
		
			if result[1] == seq:	#If sequence numbers match, we are done
				print('CheckSums Match, Seq Matches (Returned ', result[1], ', expected ', seq, ')')
				print(' ')
			
			else:	#Otherwise the server received corrupt data or our packet was lost, so resend
				print('CheckSums Match, Seq Does Not Match (Returned ', result[1], ', expected ', seq, ')')
				print('Resending...')
				RDT(data, seq)	#Resend using RDT method

		else:	#If checksums do not match, we received corrupt data, so resend
			print('CheckSums Do Not Match, Data Corrupt')
			print('Resending...')
			RDT(data, seq)	#Resend
			
	else:	#If we did get a timeout, retry
		print('Packet Timed Out, Resending...')
		RDT(data, seq)	#Recall RDT function
		
	return
	
"""
Method to send data to client
Takes sequence and data as parameters
"""
def RDTSend(seq, data):

	chksum = computeCheckSum(0, seq, data)	#Compute check sum of passed data

	values = (0, seq, data, chksum)	#Create list of data to send
	UDP_Packet_Data = struct.Struct('I I 8s 32s')	#Define structure of data
	UDP_Packet = UDP_Packet_Data.pack(*values)		#Pack the data

	#Send the UDP Packet
	UDP_IP = "127.0.0.1"	#Server IP and Port
	UDP_PORT = 5005	
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#Create Socket
	sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))	#Send via UDP Socket
	print('Packet sent: ', values)	#Display message
	
"""
Method to receive a reply from server
Will return either a string indicating we timed out or the received data packet
"""
def RDTWait():

	#Define structure of received data
	unpacker = struct.Struct('I I 8s 32s')	
	
	#Open a socket to listen on
	UDP_IP = "127.0.0.1"	
	UDP_PORT = 6006
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))
	sock.settimeout(0.009)	#Create Timer
	"""
	The above method creates a timer of 9ms that will expire if no packet is received
	Upon timeout an exception is thrown, which we catch and use to indicate to caller
	that we timed out
	"""

	try:
	#Receive data from server
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		UDP_Packet = unpacker.unpack(data)	#Unpack Data
		#print('Message received from ', addr)
		print('Packet Received: ', UDP_Packet)
		return UDP_Packet	#Return the unpacked data
		
	except socket.timeout:	#If the socket times out, catch the error and return a string
		return "Timeout"


"""## MAIN CLIENT CODE ##"""

UDP_IP = "127.0.0.1"	#Server IP
UDP_PORT = 5005			#Server Port

#Display connection info
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("")

#Create list of data to send
data = (b'NCC-1701',b'NCC-1664',b'NCC-1017')
seq = 0	#Inital sequence number

#Loop through all data to send
for d in data:
	RDT(d,seq)	#Send data via RDT method
	seq = (seq + 1) % 2	#Flip sequence number

print('All Data Sent. Exiting')


"""
3357 Assignment 4, UDP_Server
Written by Ben Dumais (250669195)
"""

import binascii
import socket
import struct
import sys
import hashlib

"""## METHODS ##"""

"""
Method to send response packet to client
Takes ack number, sequence number, and data as parameters
"""
def reply(ack, seq, data):

	#Client IP and Port
	UDP_IP = "127.0.0.1"
	UDP_PORT = 6006

	chksum = computeCheckSum(ack, seq, data)	#compute the checksum for the given data
	
	values = (ack, seq, data, chksum)	#Create datagram from passed values and check sum
	UDP_Packet_Data = struct.Struct('I I 8s 32s')	#Define structure of data
	UDP_Packet = UDP_Packet_Data.pack(*values)		#Pack Data

	#Send the UDP Packet
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
	print('Packet sent: ', values)	#Display sent packet
	print(' ')

"""
Method to compute Checksum value from passed data
Takes ack number, sequence number, and data as parameters
"""
def computeCheckSum(a, s, d):
	data = (a,s,d)	#Put passed data into a sequence
	UDP_Data = struct.Struct('I I 8s')	#Define Structure
	packed_data = UDP_Data.pack(*data)	#Pack Data
	chksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")	#Calculate bytes
	return chksum

"""## MAIN SERVER CODE ##"""

#Define Server IP and Port	
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

unpacker = struct.Struct('I I 8s 32s')	#Define unpacker structure

expSeq = 0	#Define expected sequence number
data = b"null"	#Define the null data for reply packets

#Create the socket and listen
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP Socket
sock.bind((UDP_IP, UDP_PORT))

sock.settimeout(10)	#Timeout function for the listening port. If no activity for 10s we close program
"""
For this assignment I used the built in timer function for sockets to simplify code. This method will throw an exception if there is no activity
on a socket for the set amount of time, which we can intercept and use
"""

print('Server Listening...')
print('')

try:	#Try until we get an interception
	while True:	#Loop until this program is terminated

		data, addr = sock.recvfrom(1024)			#Listen on the defined socket
		UDP_Packet = unpacker.unpack(data)			#unpack the data we received
		print("Received from", addr)				#Display client info
		print("Received message", UDP_Packet)		#Display the received data
		
		#Create the Checksum for comparison
		chksum = computeCheckSum(UDP_Packet[0], UDP_Packet[1], UDP_Packet[2])
		
		#Compare Checksums to test for corrupt data
		if UDP_Packet[3] == chksum:	#If check sums match, data was not corrupt

			#Next we check to see if we received the proper sequence numbers
			if UDP_Packet[1] == expSeq:
				print('Checksums and Sequences Match Expected Values')	#If yes, display message
				reply(1, UDP_Packet[1], data)	#Reply with the sent sequence number
				expSeq = (expSeq + 1) % 2		#Flip the expected sequence number so we can compare the next packet
				
			else:	#Same as above, but notify that it was an unexpected sequence
				print('Checksum Match, But Unexpected Sequence Number')
				reply(1, UDP_Packet[1], data)	#Reply with the same Seq and ACK it (ie, its still good just unexpected Seq)
				"""
				This part of the code is used to show that a reply packet was corrupt or never received by the client. Useful to track delays
				"""
			
		else:	#Otherwise we need to reprompt client to resend as it was corrupt
			print('Checksums Do Not Match: Packet Corrupt')
			reply(0, (UDP_Packet[1] + 1) % 2, data)	#Reply with flipped sequence number
			
except socket.timeout:	#Catch a timeout exception and exit the program.. Added to help automatically reset the server
	print('No requests for 10s, closing...')
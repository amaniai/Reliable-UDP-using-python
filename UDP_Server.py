import socket
import time
from struct import *
from simplecrypt import encrypt, decrypt
from cryptography import *
from Crypto.Cipher import AES
from Crypto.Cipher import *
import base64

import sys #Import sys module to handle command line arguments
PORT = (int(sys.argv[1]))  #Get port number from command line and convert it to integer
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Create UDP socket
s.bind(('',PORT)) #Bind the port number to the socket 
filerecieved=open("output/RecievedUDP.zip","wb") #In output folder, Open file to write recived data
packed_data, addr = s.recvfrom(calcsize('ii4096s')) #Recieve the first data chunk from address
password='this is password'
data=unpack('=ii4096s',packed_data) #unpack the recived data
print data[0] , data[1]
ack1 = str(data[0]) #get the packet seq from header
seq=0
se=str(seq)
ack = pack('i',seq) #send ack to client
msg=data[2]
#msg=decrypt(password,(data[2])) ####decrypt the msg using key
starting_time=time.time()
########check if the first packet in sequnce and write to the file####
if ack1 == se:
		print "packet in order ack will be sent",len(data[2]), "ack=" , ack1
		filerecieved.write(msg) #Write the recived data
		s.sendto(ack,(addr))
		seq+=1
else :
	print "packet dropped , out of order" , ack1 , se , seq , ack
	s.sendto(ack,(addr))
canwrite=True
#recwin=[recelement]
while True and canwrite: #Write the remainnig recieved chunks to the output file
			packed_data, addr = s.recvfrom(calcsize('ii4096s')) #Recieve the first data chunk from address
			#packed_data= password.decrypt(ciphertext)
			data=unpack('=ii4096s',packed_data)
			ack1 = data[0]
			msg=data[2]
			#msg=decrypt(password,(data[2])) ####decrypt the msg using key
			ending_time=time.time()
			print "recived seq is:", ack1 ,"my seq is:", seq
			########check if the first packet in sequnce and write to the file####
			if ack1 == seq:
				print "packet in order ack will be sent is nu" , "ack=" , ack1 , len(data[2])
				print "seq nu is",seq
				###to count the time needed to recive the file###
				print " time started reciveing:",starting_time , "time last packet recived:",ending_time
				filerecieved.write(msg) #Write the recived data
				ack = pack('i',ack1)
				s.sendto(ack,(addr))
				seq+=1
			else :
					print "packet dropped , out of order"
					print "recived seq is:", ack1 ,"my seq is:", seq
					s.sendto(ack,(addr))
					print " Last one I recived is " , data[0]
					print " time started reciveing:",starting_time , "time last packet recived:",ending_time
					
				 		
		
							
print "finish"
filerecieved.close()
s.close() #close socket



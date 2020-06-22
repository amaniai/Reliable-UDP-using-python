import socket
import sys #Import sys module to handle command line arguments
PORT = (int(sys.argv[1]))  #Get port number from command line and convert it to integer
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Create UDP socket
s.bind(('',PORT)) #Bind the port number to the socket 
filerecieved=open("output/RecievedUDP.pdf","wb") #In output folder, Open file to write recived data
data, addr = s.recvfrom(1024*4) #Recieve the first data chunk from address
filerecieved.write(data) #Write the recieved data

while True : #Write the remaining recieved chunks to the output file
	data, addr = s.recvfrom(1024*4)
	filerecieved.write(data)
	print "Writing file From:",addr
	print "file has been written"
 s.close() #close socket


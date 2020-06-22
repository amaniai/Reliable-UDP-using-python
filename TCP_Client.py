import socket
import sys #import sys module to handle command line arguments
HOST = sys.argv[1] #Get the host adress from command line
PORT = (int(sys.argv[2])) #get the port number from command line and to convert it to integer
Filetosend = (sys.argv[3])#Getthe name of the file to be sent to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create TCP client socket
s.connect((HOST, PORT)) #Establish a connection
originalfile=open("input/"+Filetosend,"rb") #open and read the file
msg= originalfile.read(1024*256)#read the first chunk of the file
s.send(msg)#send the chunk through connection
while msg : #send the remaining file chunks
	msg= originalfile.read(1024*256)
	s.send(msg)
	print "sending file to:", HOST
print "file sent"#to indicate that the file is completly sent
s.close()#close the socket


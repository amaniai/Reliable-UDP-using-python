import socket
import sys #Import sys module to handle command line arguments
PORT = (int(sys.argv[1])) #Get port number from command line and convert it to integer          
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create TCP socket
s.bind(('', PORT))#Bind the port number to the socket 
s.listen(1) #TCP server listen on port for connection requests from client
conn, addr = s.accept() #Establish the connection
filerecieved=open("output/RecievedTCP","wb")#In output folder, Open file to write recieved data
data = conn.recv(1024*256)#Recieve the first data chunk from address
filerecieved.write(data)#Write the recived data
while True:#Write the remainnig recieved chunks to the output file
    data = conn.recv(1024*256)
    filerecieved.write(data)
    if not data: break #If data is empty break the loop
    print 'Recieving message From:',addr
print "file successfully Recieved"
conn.close() #close the connection
s.close() #close socket



#########################################################
No references added to report because nothing needed, for learning I just used Youtube...
########################################################
####Instructions####
To run each test write the following commands in terminal
##############################################
1.Transferring file using UDP Sockets:
1.1 UDP_Server.py :
First run the server and provide a port number to listen such as:
 $python UDP_Server.py 5522
1.2 UDP_Client.py :
In client provide the IP address of server ,port number , name of the file you want to transfer such as:
 $python UDP_Client.py 10.0.2.4 5522 Book.pdf
###############################################
2.Transferring file using TCP Sockets:
2.1 TCP_Server.py :
First run the server and provide a port number to listen such as:
 $python TCP_Server.py 5544
2.2 TCP_Client.py :
In client provide the IP address of server ,port number , name of the file you want to transfer such as:
 $python TCP_Client.py 10.0.2.4 5544 Book.pdf
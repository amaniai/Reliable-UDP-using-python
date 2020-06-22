import socket
from struct import *
import threading
import time
from simplecrypt import encrypt,decrypt
from cryptography import *
import sys #import sys module to handle command line arguments
HOST = sys.argv[1] #Get the host adress from command line
PORT = (int(sys.argv[2])) #get the port number from command line and to convert it to integer
Filetosend = (sys.argv[3]) #Getthe name of the file to be sent to the server
addr=HOST,PORT
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Create UDP client socket
password='this is password'

#timer=threading.Timer(1.0,mytimer)
mss=1 #maximum segment size (1024*4, one packet )######
cwnd=1*mss ####intial congestion window size#####
packetno=1 #to count packets in sender window
winelement=0 # window element to be appended 
seq=0 #sequence numbers for ordering
seqwin=[seq] #sequence numbers window
rtt=0.401085138321 ###sample round trip time
retransm=0 #initial no of retransmissions
touts=0 #initial no of timeouts
	
##############timer##############
def mytimer():
	#sretransm=retransm
	cwnd=1 ### set the cwnd to 1 for timeout
	print ("timout , packet resending seq=", seq )
	print "cwnd is:", cwnd
	addr=HOST,PORT
	########send the lost packet again##########
	#timeout4=threading.Timer(3,mytimer)
	#timeout3.join()
	#print " I Send you packet with seq=",seq
	print "No of Retransmissions:",retransm , "No of Timeouts:", touts
	print "window resending"
	for winelement in window:
			s.sendto(winelement,(addr))
			#ack, addr = s.recvfrom(calcsize('i'))
			#ack1=unpack('i',ack)
			#print "No of Retransmissions:",retransm , "No of Timeouts:", touts
	cansend=True
	timeout1.cancel()
#touts+=1
#timeo=timeo+1
#######to print the cwnd ######
cwndwindow=[]
cwndwindow.append(cwnd)		
###########Establish Connection############	 	 	
originalfile=open("input/"+Filetosend,"rb") #open and read the file
msg= originalfile.read(1024*4) #read the first chunk of the file
data=msg
window=[] #Window to buffer packed data
#data=encrypt(password,msg) #Encrypting the msg
length=len(data)
#########Create Header and add it to the packet#######
packed_data= pack('ii4096s',seq , length ,data)	
#ciphertext=encrypt('Amani', packed_data)	
s.sendto(packed_data,(addr)) #send the packed data to address
print "packet 0 sent"
####Start the timer########
timeout1=threading.Timer(6,mytimer)
timeout1.start()
#######Recive ack from server########
ack, addr = s.recvfrom(calcsize('i'))
ack1=unpack('i',ack)
if ack1[0] == seq:
		print "ack recieved connection established"
		timeout1.cancel()
		cwnd=cwnd*2
		sucsess=1
else:
	s.sendto(packed_data,(addr))
	window.append(packed_data)
	print "packet resent"
	cwnd=1
	timeout1.cancel()
cwndwindow.append(cwnd)	
########counters#######
packetcount=0 #to count the total no of packets sent
countdubacks=0 # to detect 3dub acks
cansend= True # to control sending proccess
threshd=16 #threshld value , 16 segments, 64 KB

###########start loop to send the file#############
while msg and cansend:
	######## the sender window size maintained by the cwnd#########
	senderwindow=range(0,cwnd+1)
	####congestion contor####
	if cwnd>=threshd:
				cwnd=cwnd+1
	elif cwnd>=100:
				 cwnd=100
	else:
		cwnd=cwnd*2
	cwndwindow.append(cwnd)	
	
	packetno=0 ####### count no of packets sent every round
	print "########sender window size is:",len(senderwindow),"and cwnd is:",cwnd+1,"#############"
	###########start sending window#########
	#while msg and cansend:		
	for packetno in senderwindow :
		
		while msg and packetno<cwnd and cansend:
		 seq+=1
		 sucsess+=1
		 msg= originalfile.read(1024*4)
		 data=msg
		 #data=encrypt(password,msg)
		 length=len(data)
		 packed_data= pack('ii4096s',seq , length ,data) ##create header and add it to chunk
		 #ciphertext=encrypt(password, packed_data)
		 s.sendto(packed_data,(addr)) #send packet
		 #timeout1=threading.Timer(5,mytimer)
		 timeout1.join()
		 startingtime=time.time()
		 winelement=packed_data
		 window.append(packed_data) ###buffer every packet sentin the a window
		 packetno+=1
		 packetcount+=1
		 seqwin.append(seq) ##seq number window
		 cansend=False
		 print "window length",len(packed_data) , "packetconut=",packetcount, "packet no in window:",packetno,"sent" , "seq=",seq , "cwnd:",cwnd
		 #########after sending the window wait for acks#########
		timeout1=threading.Timer(0.01,mytimer)
		timeout1.start()
		ack, addr = s.recvfrom(calcsize('i'))
		endingtime=time.time()
		ack1=unpack('i',ack)
		###check if recived ack in sequence (Cumliative ack) or there is a packet loss###
		print "No of Retransmissions:",retransm , "No of Timeouts:", touts , "success", sucsess
		if ack1[0] >= seq :	
				 print "ack no" ,ack1[0] ,"is recieved , seq=" ,seq 
				 print "window length is" , len(window)
				 print "cwnd=" , cwnd , "and mss=" , mss
				 print "rtt is",rtt
				 sucsess+=1
				 #timeout1.cancel()
				 if cwnd>=threshd:
					  cwnd=cwnd+1
				 else:
					  cwnd=cwnd*2
				 timeout1.cancel()
				 cansend= True
				 #cwndwindow.append(cwnd)	
			#############Check for three dublicate acks###########
		else:	 
				 countdubacks+=1
				 #cwnd=1
				 #if cwnd>=threshd:
					  #cwnd=cwnd+1
				 #cwndwindow.append(cwnd)	
				 timeout1.cancel()
				 if countdubacks==3:
					 cwnd=cwnd=1
					 retransm+=1
					 print "3 dub acks detected , packet:",ack1[0]+1, "lost, Resend it again"
					 for winelement in window:
							print "window resending , lost packet:",ack1[0]
							s.sendto((winelement),(addr))
					 ack, addr = s.recvfrom(calcsize('i'))
					 ack1=unpack('i',ack)
							#print "No of Retransmissions:",retransm , "No of Timeouts:", touts
					 if ack1[0] == seq :
								#retransm+=1
								countdubacks=0
								if cwnd>=threshd:
									cwnd=cwnd+1
								else:
									cwnd=cwnd*2
								#cwndwindow.append(cwnd)	
								timeout1.cancel()
								cansend=True
								
								break
							#timeout2=threading.Timer(3,mytimer)
					 else:
								timeout1.cancel()
								
								#cansend=True
								cwnd=1
								countdubacks=0
				 else:
					 #timeout1=threading.Timer(3,mytimer)
					 #timeout1.start()
					 touts+=1
					 print "continue..."
					 #cansend=True
					 #continue
		#except:
			#print " what's happenn"
			
		#print "##### window recived , cum ack no" ,ack1[0] ,"arrived , my seq=" ,seq,"#####"
 
		
	cansend=True
print "CWND" , cwndwindow
print "No of Retransmissions:",retransm , "No of Timeouts:", touts	, "Success:",sucsess			
print "window length",len(window) , "packetconut=",packetcount, "packet no in window:",packetno,"sent" , "seq=",seq , "cwnd:",cwnd
#s.close() #close the socket

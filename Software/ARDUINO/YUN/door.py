#!/usr/bin/python
import serial, time, socket, sys, telnetlib
sys.path.insert(0,'/usr/lib/python2.7/bridge/')
sys.path.insert(0,'/usr/lib/python2.7/socket/')
from bridgeclient import BridgeClient as bridgeclient

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(('',8888))

print("UDPServer listening on port 8888")

###Device Characteristics
##DOOR LOCK
ID='DOR003'
NET='WF'
TYPE='00A'
STATE='0'
SP='SP'
LOCK='0'

while True:
	data, address=sock.recvfrom(1024)

	print ("Received message: ",  data)
	print ("Received from: ", address)

	if (data == "SERVER BROADCAST"):
		msg="SERVER BROADCAST"
	elif (data == "DISCOVER"):		
		msg='ID' + ID + SP + NET + SP + TYPE + SP + STATE + SP + LOCK
	elif (data == "SET ON"):
		STATE='1'
		msg='ACK' + STATE	
                HOOST= "localhost"
                PORT=6571
                try:
                        tn=telnetlib.Telnet(HOOST,PORT,5)
                except socket.timeout:
                        pass
                tn.write(STATE + "\n")
                tn.write("exit\n")
                tn.close()

	elif (data == "SET OFF"):
		STATE='0'
		msg='ACK'+ STATE
              	HOOST= "localhost"
                PORT=6571
                try:
                        tn=telnetlib.Telnet(HOOST,PORT,5)
                except socket.timeout:
                        pass
                tn.write(STATE + "\n")
                tn.write("exit\n")
                tn.close()

	elif (data == "SET TOGGLE"):
		if (STATE=="1"): STATE='0'
		else: STATE='1'
		msg='ACK' + STATE
		HOOST= "localhost"
		PORT=6571
		try:
                        tn=telnetlib.Telnet(HOOST,PORT,5)
                except socket.timeout:
                        pass
                tn.write(STATE + "\n")
                tn.write("exit\n")
                tn.close()

	elif (data == "SET LOCK"):
		LOCK='1'
		msg='ACK' + LOCK
	elif (data == "SET UNLOCK"):
		LOCK='0'
		msg='ACK' + LOCK
	elif (data == "REFRESH"):
		msg='REF' +  STATE + SP + LOCK
	else:
		msg="ACK"
		print("(",address[0],"",address[1]," )said: ", data) 
	sock.sendto(bytes(msg),address)
	print("After data")

sock.close()


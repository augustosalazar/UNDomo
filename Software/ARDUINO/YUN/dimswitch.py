#!/usr/bin/python
import serial, time, socket, sys, telnetlib
sys.path.insert(0,'/usr/lib/python2.7/bridge/')
sys.path.insert(0,'/usr/lib/python2.7/socket/')
from bridgeclient import BridgeClient as bridgeclient

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(('',8888))

#Console=Console.Console()
#ser=serial.Serial('/dev/ttyATH0',9600)
#entrada=raw_input('Introduce un caracter: ')
#ser.write(entrada)
#print ("He enviado ", entrada)
#ser.close()

print("UDPServer listening on port 8888")

###Device Characteristics
##DIMMER SWITCH
ID='DMS032'
NET='WF'
TYPE='104'
STATE='0'
MAX='1'
MIN='0'
VALUE='0.5'
SP='SP'

while True:
	data, address=sock.recvfrom(1024)

	print ("Received message: ",  data)
	print ("Received from: ", address)

	if (data == "SERVER BROADCAST"):
		msg="SERVER BROADCAST"
	elif (data == "DISCOVER"):		
		msg='ID' + ID + SP + NET + SP + TYPE + SP + STATE + SP + MAX + SP + MIN + SP + VALUE
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

	elif (data.startswith("SET VALUE")):
		fin=len(data)
		VALUE=data[9:fin]
		msg='ACK' + VALUE

	elif (data == "REFRESH"):
		msg='REF' +  STATE + SP + VALUE
	else:
		msg="ACK"
		print("(",address[0],"",address[1]," )said: ", data) 
	sock.sendto(bytes(msg),address)
	print("After data")

sock.close()


        

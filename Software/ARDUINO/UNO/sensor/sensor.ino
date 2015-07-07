
/*
  WiFi UDP Send and Receive String
 
 This sketch wait an UDP packet on localPort using a WiFi shield.
 When a packet is received an Acknowledge packet is sent to the client on port remotePort
 
 Circuit:
 * WiFi shield attached
 
 created 30 December 2012
 by dlf (Metodo2 srl)

 */


#include <SPI.h>
#include <WiFi.h>
#include <WiFiUdp.h>

int status = WL_IDLE_STATUS;
char ssid[] = "routerWinter2013"; //  your network SSID (name) 
char pass[] = "24681012";    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key Index number (needed only for WEP)

unsigned int localPort = 8888;      // local port to listen on

char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet
char  ReplyBuffer[80];       // a string to send back
char ReplyBroad[]= "SERVER BROADCAST";
char ReplyDiscover[80];
//Device Characteristics
char ack[] = "ACK";
char idd[] = "ID";
char ref[] = "REF";
char id[] = "SSN456";
char net[] = "WF";
char type[] = "00C";
char sp[] = "SP";
char state[] = "0"; 

WiFiUDP Udp;

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);   
  
  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present"); 
    // don't continue:
    while(true);
  } 
  
  // attempt to connect to Wifi network:
  while ( status != WL_CONNECTED) { 
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:    
    status = WiFi.begin(ssid, pass);
  
    // wait 10 seconds for connection:
    delay(10000);
  } 
  Serial.println("Connected to wifi");
  printWifiStatus();
  
  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  pinMode(13,OUTPUT);
  Udp.begin(localPort);  
  Serial.print("Listening Local Port ");
  Serial.print(localPort);  
}

void loop() {

  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if(packetSize)
  {   
    Serial.print("\nReceived packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remoteIp = Udp.remoteIP();
    Serial.print(remoteIp);
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
    if (len >0) packetBuffer[len]=0;
    Serial.println("Contents:");
    Serial.println(packetBuffer);
    
    // send a reply, to the IP address and port that sent us the packet we received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    
    if(strcmp(packetBuffer,"DISCOVER") == 0){
      sprintf(ReplyDiscover,"%s%s%s%s%s%s%s%s",idd,id,sp,net,sp,type,sp,state);
      Udp.write(ReplyDiscover);
      Serial.println("Msg: Discovery "); 
    }
    //SET ON COMMAND 
    else if(strcmp(packetBuffer,"SET ON") == 0){
      digitalWrite(13, HIGH);
      char state[]= "1";
      sprintf(ReplyBuffer,"%s%s",ack,state);
      Udp.write(ReplyBuffer);
    }
    // SET OFF COMMAND
    else if (strcmp(packetBuffer,"SET OFF") == 0){
      digitalWrite(13, LOW);
      char state[]= "0";
      sprintf(ReplyBuffer,"%s%s",ack,state);
      Udp.write(ReplyBuffer);
    }
   
    //Broadcast from server
    else if(strcmp(packetBuffer,ReplyBroad) == 0){
      Udp.write(ReplyBroad);
      Serial.println("Msg: Broadcast ");
    }    
    else{
      Udp.write(ack);
      Serial.println("Msg: Unicast ");
    }    
    Udp.endPacket();
   }
}


void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}





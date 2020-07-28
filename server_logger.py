'''
This script written for testing client server logic for socket for multithreading
Logic for my client side ----->if received msg has '35' then i need to send yes flag to client side
then it will send me hexdata
Tested for: Teldev_Zest
'''
import binascii
import socket, threading
import time 
from datetime import datetime
import os
from logger import Logger

debug_mode = 0
debug_enable = 0
logFile = "serverdatalog.log"
logger = Logger(log_file=(__file__.split(".")[0] + str(".log")), mode=1, debug=1)


def loginfo(msg):
    #loginfo (self.mode,self.debug,"loginfo"):
    #msg=str(self.tag)+" :"+msg
    #try:
    msg = str(msg)
    #except:
    #msg = msg.encode('utf-8')
    logger.log(msg)


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket,thread_id):
        threading.Thread.__init__(self)
        self.threadID = thread_id
	self.csocket = clientsocket
	StartTime = datetime.now()
        strDateTime = StartTime.strftime('%Y-%m-%d %H:%M:%S')
        loginfo ("New connection added by client address"+str(clientAddress))
    def run(self):
        loginfo ("Connection from thread:"+str(thread_id)+str(clientAddress))
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            #CurrentTime = datetime.now()
	    #strDateTime = CurrentTime.strftime('%Y-%m-%d %H:%M:%S')
	    #loginfo(strDateTime+":"+ "\tThread:\t"+str(thread_id)+str(clientAddress[1])+"\tThread Started...")
	    loginfo("Thread Started...")
	    data = self.csocket.recv(50*2048)
            loginfo("Received Data1\n"+str(data))
	    #msg = data.decode()
            if data != '':
	         #CurrentTime = datetime.now()
                 #strDateTime = CurrentTime.strftime('%Y-%m-%d %H:%M:%S')
	         hexdata = binascii.hexlify(data)
                 loginfo("Received HexData1:\n"+str(hexdata))
                 if '35' in data:
	           imei = data
	           #CurrentTime = datetime.now()
                   #strDateTime = CurrentTime.strftime('%Y-%m-%d %H:%M:%S')
                   loginfo("Thread:\t"+str(clientAddress[1])+"\t received imei:"+str(imei))
                   self.csocket.send('\x01')
	           loginfo("sent yes flag i.e 0x01")
	    else:
	         loginfo("Thread:\t"+str(clientAddress[1])+"\nno data received")
	         time.sleep(10)
	         #loginfo(strDateTime +":"+ "\tThread:\t"+str(clientAddress[1])+"\t checking for data:")  
	         break
	loginfo("Thread:\t"+str(thread_id)+str(clientAddress[1])+"\tclient disconnected...")

	def stop(self, Mode=0):
            global threads
            loginfo("Inside stop thread")
            try:
                self.csocket.shutdown(2)
                loginfo("Connection shutdown")
            except Exception as e:
                loginfo("Error in connection shutdown " + str(e))
            try:
	    
                self.csocket.close()
                loginfo("Connection closed")
            except Exception as e:
                loginfo("Error in connection close " + str(e))
	    try:
                threads.remove(self)
                loginfo("Thread list removed")
            except:
                loginfo("Error in removing thread from list")

if __name__ == "__main__":        
 	serveraddr='ec2-34-216-237-202.us-west-2.compute.amazonaws.com'
 	LOCALHOST = "127.0.0.1"
	PORT = 10006
	thread_id = 0
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind((serveraddr, PORT))
	loginfo("Server started")
	loginfo("Waiting for client request..")
	global threads 
	threads = []
	while True:
    	    try:
		server.listen(5)
    	    	clientsock, clientAddress = server.accept()
    	    	#clientsock.setblocking(0)
    	    	newthread = ClientThread(clientAddress, clientsock,thread_id)
    	    	thread_id += 1
    	    	threads += [newthread]
    	    	newthread.start()
	    except Exception as e:
            	server.close()
		loginfo("Exception in socket"+str(e))
		break
	server.close()
	os._exit(1)


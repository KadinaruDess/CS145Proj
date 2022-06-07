import socket
import time
import random
import string
import re
import hashlib

# THIS setup
MY_HOSTNAME = socket.gethostname()
MY_IP = socket.gethostbyname(MY_HOSTNAME)
MY_PORT = 9000

IS_DEBUG = True

# OTHER setup
OTHER_IP = MY_IP
OTHER_PORT = 6741

# Setting up UDP socket
UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPsocket.bind(('',MY_PORT))

# Sends an ascii msg to OTHER
def UDP_sendmsg(msg):
    if (IS_DEBUG):
        print("[sent msg:] " + msg)
    UDPsocket.sendto(msg.encode('ascii'), (OTHER_IP,OTHER_PORT))

# Recieving a UDP ascii msg
def UDP_getmsg():
	while True:
		data, addr = UDPsocket.recvfrom(1024)
		if len(data) > 0:
			msg = data.decode('ascii')
			if (IS_DEBUG):
				print("[recieved msg:] " + msg)
			return msg

# Parses a payload message for information using RegEx
def parsePayload(msg):
	ID = re.search(r"ID.{8}",msg).group()[2:]
	SN = int(re.search(r"SN.{7}",msg).group()[2:])
	TXN = int(re.search(r"TXN.{7}",msg).group()[3:])
	LAST = int(re.search(r"LAST[01]",msg).group()[4:])
	PAYLOAD = re.search(r"LAST[01].*",msg).group()[5:]

	print("Parsed Payload: ",end='')
	print(ID,SN,TXN,LAST,PAYLOAD)
	return (ID,SN,TXN,LAST,PAYLOAD)

# Gets checksum of the string msg
def getChecksum(msg):
    return hashlib.md5(msg.encode('utf-8')).hexdigest()

# Encodes the parameters to the given ACK format
def encodeAck(seqNo,transaction,checksum):
    msg = 'ACK' + str(seqNo).zfill(7) + 'TXN' + str(transaction).zfill(7) + 'MD5' + checksum
    return msg

# Initiating transaction
UDP_getmsg()
randTransactionID = ''.join(random.choices(string.digits, k=7))
print("Generated Transaction ID: " + str(randTransactionID))
UDP_sendmsg(randTransactionID)

while True:
	packet = UDP_getmsg()
	ID,SN,TXN,LAST,PAYLOAD = parsePayload(packet)
	ack = encodeAck(SN,randTransactionID,getChecksum(packet))
	UDP_sendmsg(ack)
	if(LAST==1): break

	

	

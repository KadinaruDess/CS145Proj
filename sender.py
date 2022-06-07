import hashlib
import re
import socket
import sys

DO_LOG = True

# PAYLOAD file name
PAYLOAD_FILENAME = "03383a1b.txt"

# THIS setup
MY_ID = "03383a1b"
MY_HOSTNAME = socket.gethostname()
MY_IP = socket.gethostbyname(MY_HOSTNAME)
MY_PORT = 6741

# OTHER setup
OTHER_IP = "10.0.7.141"
OTHER_PORT = 9000

# Setting up UDP socket
UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPsocket.bind(('',MY_PORT))

# Sends an ascii msg to OTHER
def UDP_sendmsg(msg):
    if (DO_LOG):
        print("[sent msg:] " + msg)
    UDPsocket.sendto(msg.encode('ascii'), (OTHER_IP,OTHER_PORT))

# Recieving a UDP ascii msg
def UDP_getmsg():
	while True:
		data, addr = UDPsocket.recvfrom(1024)
		if len(data) > 0:
			msg = data.decode('ascii')
			if (DO_LOG):
				print("[recieved msg:] " + msg)
			return msg

# Opens and returns all contents of PAYLOAD_FILENAME
def readFile():
    with open(PAYLOAD_FILENAME,encoding='ascii') as f:
        contents = f.read()
        return contents

# Splits a msg string by i characters, and returns the split string as a tuple
def splitString(msg, i):
    if i >= len(msg):
        return (msg,'')
    if i <= 0:
        return ('',msg)
    
    first = msg[:i]
    second = msg[i-len(msg):]
    
    return (first,second)

# Encodes the payload and parameters to the given message format
def encodePayload(seqNo, transaction, isLast, payload):
    Z = '1' if isLast else '0'
    msg = 'ID' + MY_ID + 'SN' + str(seqNo).zfill(7) + 'TXN' + str(transaction).zfill(7) + 'LAST' + Z + payload
    return msg

# Gets checksum of the string msg
def getChecksum(msg):
    return hashlib.md5(msg.encode('utf-8')).hexdigest()

# Parses an ACK message for information using RegEx
def parseAck(msg):
    SN = int(re.search(r"ACK.{7}",msg).group()[3:])
    TXN = int(re.search(r"TXN.{7}",msg).group()[3:])
    CHECKSUM = re.search(r"MD5.*",msg).group()[3:]
	
    if (DO_LOG):
        print("Parsed Ack: ",end='')
        print(SN,TXN,CHECKSUM)

    return (SN, TXN, CHECKSUM)

# Initiates transaction and returns the transaction ID
def startTransaction():
    intentMessage = "ID" + MY_ID
    UDP_sendmsg(intentMessage)
    transaction = int(UDP_getmsg())
    if (DO_LOG):
        print("Transaction ID: " + str(transaction))
    return transaction

# Basic automated sending of the contents
# Segments contents by equally sized packets
# Waits for Ack before sending next packet
def ConstantSizeSend_WaitForAck(contents,transaction,bytes):
    seqNo = 0
    while(contents):

        # Split the defined size of characters from the contents
        payload, contents = splitString(contents,bytes*2)

        # Check if the segmentation is the last 
        isLast = (contents=='')

        # Encode the segmentation to a packet as per the parameters
        encodedMsg = encodePayload(seqNo,transaction,isLast,payload)

        # Sending the UDP message
        UDP_sendmsg(encodedMsg)

        # Recieving the ACK message
        ack = UDP_getmsg()
        SN, TXN, CHECKSUM = parseAck(ack)        
        
        # Increase the sequence number 
        seqNo+=bytes
            
# Processing Inline Arguments
if (DO_LOG):
    print('[Inline Command Line]',end=' ')
    for i in sys.argv:
        print(i,end=' ')
    print('')

if '-f' in sys.argv:
    idx = sys.argv.index('-f') + 1
    PAYLOAD_FILENAME = sys.argv[idx]

if '-a' in sys.argv:
    idx = sys.argv.index('-a') + 1
    OTHER_IP = sys.argv[idx]
    
if '-s' in sys.argv:
    idx = sys.argv.index('-s') + 1
    OTHER_PORT = int(sys.argv[idx])

if '-c' in sys.argv:
    idx = sys.argv.index('-c') + 1
    MY_PORT = int(sys.argv[idx])
    
if '-i' in sys.argv:
    idx = sys.argv.index('-i') + 1
    MY_ID = sys.argv[idx]

contents = readFile()
transaction = startTransaction()
ConstantSizeSend_WaitForAck(contents,transaction,1)

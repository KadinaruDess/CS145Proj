Adrian Joshua M. Reapor
CS 145 Project (June 6, 2022)

Implementation Level: 1
	- Can send Intent Messages to a receiver
	- Can receive the Accept Message reply.

=== Dependencies ===
OS Version Used: Ubuntu (test server experiments), WSL (self-testing experiments)

=== Setup ===
execution (flags in any order):
python3 sender.py [-f <PAYLOAD_FILENAME>] [-a <RECIEVER_IP_ADDR>] [-s <RECIEVER_PORT>] [-c <SENDER_PORT>] [-i <UNIQUE_ID>]

=== Included Files ===
1. sender.py

2. /payloads/payloadX.txt
	- payloads used for experiment X
	
3. /captures/captureX.pcap
	- tshark tracefiles for experiment X

4. /logs/logX.txt
	- recorded console log for experiment X

5. reciever.py
	- used for self-testing sender.py (run sender.py with -a option being the sender IP address, or "''")

*note that X stands for multiple files valuing from 1 to 5

=== How To Use ===
1. Executed through the command line "python 3 sender.py [flag/s]", with the flags being optional.
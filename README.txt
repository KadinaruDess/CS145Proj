Adrian Joshua M. Reapor
CS 145 Project (June 6, 2022)
Parameter-Adaptive Reliable UDP-based Protocol

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
	- used for self-testing sender.py

*note that X stands for multiple files valuing from 1 to 5

=== How To Use ===
1. sender.py is executed through the command line "python3 sender.py [flag/s]", with the flags being optional.
2. For self testing with reciever.py, run reciever.py first through command line "python3 reciever.py", then in another terminal run "python3 sender.py -a '' ".
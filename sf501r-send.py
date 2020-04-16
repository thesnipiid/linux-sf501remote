from sf501remote import *
import sys

DATA_PIN    = 25     # BROADCOM number of the gpio pin connected to the 433.9MHz RX
PROTOCOL_ID = 0x1035 # ID used by the protocol, to be changed with yours ID.

Send = SF501R(PROTOCOL_ID,DATA_PIN)
if sys.argv[1] == "all":
    print("switching all socket to : " , sys.argv[2])
    Send.switch_all(int(sys.argv[2]))
elif sys.argv[1] == "ch":
    print("switching socket ",sys.argv[2]," to : " , sys.argv[3])
    Send.send_command(int(sys.argv[3]),int(sys.argv[2]))

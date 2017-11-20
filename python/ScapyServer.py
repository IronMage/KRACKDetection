import scapy
import unittest
from ScapyPlaybook import ScapyPlaybook

"""
RELATED SCAPY MODES
    Dot11           : <member 'name' of 'Packet' objects>
    Dot11ATIM       : <member 'name' of 'Packet' objects>
    Dot11AssoReq    : <member 'name' of 'Packet' objects>
    Dot11AssoResp   : <member 'name' of 'Packet' objects>
    Dot11Auth       : <member 'name' of 'Packet' objects>
    Dot11Beacon     : <member 'name' of 'Packet' objects>
    Dot11Deauth     : <member 'name' of 'Packet' objects>
    Dot11Disas      : <member 'name' of 'Packet' objects>
    Dot11Elt        : <member 'name' of 'Packet' objects>
    Dot11ProbeReq   : <member 'name' of 'Packet' objects>
    Dot11ProbeResp  : <member 'name' of 'Packet' objects>
    Dot11QoS        : <member 'name' of 'Packet' objects>
    Dot11ReassoReq  : <member 'name' of 'Packet' objects>
    Dot11ReassoResp : <member 'name' of 'Packet' objects>

CVE List
    1-Key Re-Install using Fast Transmit 
    2-Already In Use Group Key Re-Install 
    3-Extended Protection of WNM-Sleep Mode
    4-Prevent Zeroed Key Install
    5-Generate New Nonce When Rekeying PTK
    6-Reject TPK-TK Reconfiguration
    7-Ignore WNM-Sleep Mode Response without pending request
    8-Do not allow multiple Reassociation Response frames

PACKET BUILDING NOTES:
[From Scapy FAQs]
I can't ping 127.0.0.1. Scapy does not work with 127.0.0.1 or on the loopback interface
---------------------------------------------------------------------------------------------------------
The loopback interface is a very special interface. Packets going through it are not really 
assembled and disassembled. The kernel routes the packet to its destination while it is still 
stored an internal structure. What you see with tcpdump -i lo is only a fake to make you 
think everything is normal. The kernel is not aware of what Scapy is doing behind his back, 
so what you see on the loopback interface is also a fake. Except this one did not come from a 
local structure. Thus the kernel will never receive it.

In order to speak to local applications, you need to build your packets one layer upper, using 
a PF_INET/SOCK_RAW socket instead of a PF_PACKET/SOCK_RAW (or its equivalent on other systems than Linux):
>>> conf.L3socket
<class __main__.L3PacketSocket at 0xb7bdf5fc>
>>> conf.L3socket=L3RawSocket
>>> sr1(IP(dst="127.0.0.1")/ICMP())
<IP  version=4L ihl=5L tos=0x0 len=28 id=40953 flags= frag=0L ttl=64 proto=ICMP chksum=0xdce5 src=127.0.0.1 
dst=127.0.0.1 options='' |<ICMP  type=echo-reply code=0 chksum=0xffff id=0x0 seq=0x0 |>>
"""

class ScapyServer():
    def __init__(self):
        #Build ScapyPlaybooks here
        self.playbook_list = []
    
    def addPlaybook(self, pb):
        self.playbook_list.append(pb)

    def run(self):
        for pb in self.playbook_list:
            pb.run()

def printPacket(p):
    print p

if __name__ == "__main__":
    #Example setup for creating a server with a single playbook and that playbook with a single play
    serv = ScapyServer()
    #Default interface is "lo", but I use the ethernet just to make sure there is some traffic to find
    pb = ScapyPlaybook(interface="enp0s3")
    play = {"MODE":1, "HANDLER":printPacket}
    pb.addPlay(play)
    serv.addPlaybook(pb)
    serv.run()







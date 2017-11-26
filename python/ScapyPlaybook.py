import unittest
from scapy.all import *
"""
Need to analyze the 802.11 layer (referred to as Dot11 in scapy).
Packet layout described here: http://www.studioreti.it/slide/802-11-Frame_E_C.pdf

RELATED SCAPY MODES (Probably easiest to rely on the type/subtype fields?)
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

NOTE:
    The send command for scapy returns the answer(s?) to the TX

PLAY FUNCTIONALITY:
    LAYOUT (DICTIONARY?):
        MODE        : Send(0) or Rcv(1)
        FILTER      : RECV ONLY (OPTIONAL) -- Used to define filter for sniffing
        PACKET      : SEND ONLY -- Packet to be sent to interface
        HANDLER     : Function to handle the response after sending packet

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

class ScapyPlaybook():
    def __init__(self, flags=[], interface="lo"):
        #Put stuff here
        self.play_list      = []
        self.allowed_flags  = flags
        self.interface      = interface
        if interface == "lo":
            print "Setting up socket for loopback"
            conf.L3Socket=L3RawSocket

    def run(self):
        #print "Starting run routine"
        for play in self.play_list:
            #sr1 is used only for layer 3 (IP, ARP, etc).  Returns only one response packet
            if play["MODE"] == 0:
                print "Sending Packet"
                response = sr1(play["PACKET"])
                play["HANDLER"](response)
            elif play["MODE"] == 1:
                #print "Sniffing Packet"
                #The filter SHOULD BE USED, as a count must be used to prevent inifinite running
                try:
                    sniff(filter=play["FILTER"], iface=self.interface, count=1, prn=play["HANDLER"])
                except KeyError:
                    sniff(iface=self.interface, count=1, prn=play["HANDLER"])

    def addPlay(self, play):
        print play
        if play and "MODE" in play:
            if (play["MODE"] == 0 and ("PACKET" in play) and ("HANDLER" in play)):
                        print "Added play"
                        self.play_list.append(play)
            if (play["MODE"] == 1 and ("HANDLER" in play)):
		        print "Added play"
                        self.play_list.append(play)
        print "Ending addPlay routine"

    def filterPacket(self, packet):
        if packet and packet.haslayer(Dot11):
            if (packet.type, packet.subtype) in self.allowed_flags:
                print "Full packet:"
                print hexdump(packet)
                print "802.11 Header"
                print hexdump(packet[Dot11])
                print "Type"
                print packet[Dot11].type
                print "Subtype"
                print packet[Dot11].subtype

    def readPCAP(self, file_name):
        #used for testing
        try:
            captures = rdpcap(file_name)
        except:
            return False

        count = 0

        for packet in captures:
            packet.show()
            self.filterPacket(packet)
            count+=1
            if count == 10:
                break

def printPacket(p):
    print p
def nothing(p):
    print ""

if __name__ == "__main__":
    """
    #Flag definitions. Format (Type, Subtype)
    flags = []
    #Type Management, Subtype Probe Request => 802.11 Probe Request
    flags.append((0, 4))
    #Type Management, Subtype Beacon => 802.11 Beacon Frame
    flags.append((0, 8))


    play = ScapyPlaybook(flags, "lo")
    play.readPCAP("example-ft.pcapng")
    """
    """
    #Just a quick test. Uses the defualt ethernet interface for Debian 9
    play_book = ScapyPlaybook(interface="enp0s3")
    play = {"MODE":1, "HANDLER":printPacket}
    play_book.addPlay(play)
    play_book.run()
    """

    pb = ScapyPlaybook()

    while(True):
        mode = raw_input("Enter 0 for send mode, 1 for recv mode")
        mode = int(mode)
        if(mode == 0 or 1):
            break

    if(mode == 0):
        play = {"MODE":mode, "HANDLER":nothing, "PACKET":(IP(dst="127.0.0.1")/ICMP())}
    else:
        play = {"MODE":mode, "HANDLER":printPacket}

    pb.addPlay(play)
    pb.run()

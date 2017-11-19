import unittest
from scapy.all import *
"""
Need to analyze the 802.11 layer (referred to as Dot11 in scapy).
Packet layout described here: http://www.studioreti.it/slide/802-11-Frame_E_C.pdf

RELATED SCAPY MODES
	Dot11      		: <member 'name' of 'Packet' objects>
	Dot11ATIM  		: <member 'name' of 'Packet' objects>
	Dot11AssoReq 	: <member 'name' of 'Packet' objects>
	Dot11AssoResp 	: <member 'name' of 'Packet' objects>
	Dot11Auth  		: <member 'name' of 'Packet' objects>
	Dot11Beacon 	: <member 'name' of 'Packet' objects>
	Dot11Deauth 	: <member 'name' of 'Packet' objects>
	Dot11Disas 		: <member 'name' of 'Packet' objects>
	Dot11Elt   		: <member 'name' of 'Packet' objects>
	Dot11ProbeReq 	: <member 'name' of 'Packet' objects>
	Dot11ProbeResp 	: <member 'name' of 'Packet' objects>
	Dot11QoS   		: <member 'name' of 'Packet' objects>
	Dot11ReassoReq 	: <member 'name' of 'Packet' objects>
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
"""

class ScapyPlaybook():
	def __init__(self, flags, interface):
		#Put stuff here
		self.allowed_flags = flags
		self.play_list = []
		self.interface = 

	def run(self):
		for play in self.play_list:
			if play[MODE] == 0:

			if play[MODE] == 1:


	def addPlay(self, play):
		self.play_list.append(play)

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

if __name__ == "__main__":
	#Flag definitions. Format (Type, Subtype)
	flags = []
	#Type Management, Subtype Probe Request => 802.11 Probe Request
	flags.append((0, 4))
	#Type Management, Subtype Beacon => 802.11 Beacon Frame
	flags.append((0, 8))


	play = ScapyPlaybook(flags)
	play.readPCAP("example-ft.pcapng")
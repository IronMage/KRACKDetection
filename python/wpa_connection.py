from ScapyPlaybook import *

def handle_beacon_resp(p):
    hexdump(p)

def main():
    """
    Steps
    play0_BeaconFrame
    play1_ProbeRequest
    play2_ProbeResponse
    play3_AuthRequest
    play4_AuthResponse
    play5_AssocRequest
    play6_AssocResponse
    play7_4WayMsg1
    play8_4wayMsg2
    play9_4WayMsg3
    play10_4WayMsg4
    """
    print "Starting"
    pb = ScapyPlaybook()
    
    SEND          = 0
    RCV           = 1
    broadcast_mac = 'ff:ff:ff:ff:ff:ff'
    my_mac        = '22:22:22:22:22:22'
    my_ssid       = 'KRACKDetection'
    my_psk        = 'KRACKPassword'
    
    #                     BeaconFrame=0,8
    dot11         = Dot11(type=0,subtype=8,addr1=broadcast_mac,addr2=my_mac,addr3=my_mac)
    #                           Example had ESS to emulate an enterpise setup, using BSS for home setup?
    beacon        = Dot11Beacon(cap='privacy')
    #Create network info
    essid         = Dot11Elt(ID='SSID',info=my_ssid,len=len(my_ssid))
    #Required for WPA2
    rsn           = Dot11Elt(ID='RSNinfo',info=(
    '\x01\x00'              #RSN v1
    '\x00\x0f\xac\x02'      #Group Cipher Suite : 00-0f-ac TKIP
    '\x02\x00'              #2 Pairwise Cipher Suites (next two lines)
    '\x00\x0f\xac\x04'      #AES Cipher
    '\x00\x0f\xac\x02'      #TKIP Cipher
    '\x01\x00'              #1 Authentication Key Management Suite (next line)
    '\x00\x0f\xac\x02'      #Pre-Shared Key
    '\x00\x00'))            #RSN Capabilities (no extra)
    
    pkt = RadioTap()/dot11/beacon/essid/rsn
    play_BeaconFrame = {"MODE":SEND, "HANDLER": handle_beacon_resp, "PACKET":pkt}
    
    print "Adding play"
    pb.addPlay(play_BeaconFrame)
    print "Running"
    pb.run()
    print "Done"
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    

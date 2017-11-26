from scapy.all import *

if __name__ == '__main__':
    pkt = RadioTap()/Dot11(type=0,subtype=4,addr1='ff:ff:ff:ff:ff:ff',addr2='11:11:11:11:11:11',
          addr3='11:11:11:11:11:11')/Dot11Auth(algo=0,seqnum=1,status=0)
          
    #conf.L3Socket=L3RawSocket
    sendp(pkt, iface="lo")

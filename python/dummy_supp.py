from scapy.all import *

if __name__ == '__main__':
    conf.L3Socket=L3RawSocket
    pkt = RadioTap()/Dot11(type=0,subtype=4,addr1='ff:ff:ff:ff:ff:ff',addr2='11:11:11:11:11:11',
          addr3='11:11:11:11:11:11')
          
    pkt.show()
    sendp(pkt, iface="lo")

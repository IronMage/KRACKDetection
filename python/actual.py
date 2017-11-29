#!/usr/bin/env pyt

import subprocess
from sys import stdin, argv, stdout
from os.path import basename

nice_list = {"FT: Do not re-install same PTK to the driver" : "CVE-2017-13077", #0001
      "WPA: Not reinstalling already in-use IGTK to the driver" : "CVE-2017-13081", #0002
      "WPA: Invalid IGTK KeyID" : "CVE-2017-13081", #0002
      "Failed to configure IGTK to the driver" : "CVE-2017-13081", #0002
      "WPA: Failed to get random data for ANonce" : "CVE-2017-", #0005
      "WPA: Assign new ANonce" : "CVE-2017-", #0005
      "TDLS: TPK-TK for the peer" : "CVE-2017-13086", #0006
      "TDLS: Configure pairwise key for peer" : "CVE-2017-", #0006
      "has already been configrued to the driver - do not reconfigure" : "CVE-2017-#", #0006
      "WNM: Ignore WNM-Sleep Mode Response frame since WNM-Sleep Mode operation has not been requested" : "CVE-2017-13088", #0007
      "FT: Reassociation has already been completed for this FT protocol instance - ignore unexpected retransmission" : "CVE-2017-13082", #0008
      }
naughty_list = [
    "WPA: Failed to configure IGTK to the driver", #0002
    "WPA: IGTK keyid %d pn %02x%02x%02x%02x%02x%02x", #0002
    "Install IGTK (WNM SLEEP)", # 0002
    "Failed to install the IGTK in WNM mode", #0002
    "WNM: Ignore WNM-Sleep Mode Response frame since WNM-Sleep Mode has not been used in this association", #0007
    ]

def printResults(vl, nvl):
    print "\nVulnerable List:"
    for item in vl :
        print item;
    print "\nNot vulnerable List:"
    for item in nvl :
        print item;


def main(command):
    print "Your command:", command

    if command == "":
        print "Must supply wpa_supplicant command"
        return 0

    vulnerable = [];
    not_vulnerable = [];

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    for line in iter(proc.stdout.readline, ''):
        for msg in nice_list:
            if msg in line:
                #Found a bad printout
                #print nice_list[msg]
                not_vulnerable.append(nice_list[msg]);
                break

        for msg in naughty_list:
            if msg in line:
                #Found a bad printout
                #print msg
                vulnerable.append(msg);
                break
    printResults(vulnerable, not_vulnerable);

if __name__ == "__main__":
    file_name = basename(__file__)
    command = ""
    for token in argv:
        if token != file_name:
            command += token + " "
    """
    if "-ddd" not in command:
        command += "-ddd"
    """

    main(command)

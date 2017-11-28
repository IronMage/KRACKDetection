#!/usr/bin/env pyt

import subprocess
from sys import stdin, argv, stdout
from os.path import basename

naughty_list = {"FT: Do not re-install same PTK to the driver" : "CVE-2017-#",
      "WPA: Failed to get random data for ANonce" : "CVE-2017-#",
      "TDLS: TPK-TK for the peer" : "CVE-2017-#",
      "has already been configrued to the driver - do not reconfigure" : "CVE-2017-#",
      "WNM: Ignore WNM-Sleep Mode Response frame since WNM-Sleep Mode operation has not been requested" : "CVE-2017-#",
      "WPA: Not reinstalling already in-use GTK to the driver" : "CVE-2017-#",
      "FT: Reassociation has already been completed for this FT protocol instance - ignore unexpected retransmission" : "CVE-2017-#",
      "CodyLentPatch3Placeholder" : "CVE-2017-#",
      "CodyLentPatch4Placeholder" : "CVE-2017-#",
      "play10_4WayMsg4" : "CVE-2017-#"}
"""
naughty_list = ["FT: Do not re-install same PTK to the driver",
                "WPA: Failed to get random data for ANonce",
                "TDLS: TPK-TK for the peer",
                "has already been configrued to the driver - do not reconfigure",
                "WNM: Ignore WNM-Sleep Mode Response frame since WNM-Sleep Mode operation has not been requested",
                "WPA: Not reinstalling already in-use GTK to the driver",
                "FT: Reassociation has already been completed for this FT protocol instance - ignore unexpected retransmission",
                "CodyLentPatch3Placeholder",
                "CodyLentPatch4Placeholder",
                "play10_4WayMsg4"]
"""



def main(command):
    print "Your command:", command

    if command == "":
        print "Must supply wpa_supplicant command"
        return 0

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    for line in iter(proc.stdout.readline, ''):
        for msg in naughty_list:
            if msg in line:
                #Found a bad printout
                print naughty_list[msg]
                break

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

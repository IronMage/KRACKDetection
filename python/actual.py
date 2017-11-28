#!/usr/bin/env pyt

import subprocess
from sys import stdin, argv
from os.path import basename

naughty_list = ["FT: Do not re-install same PTK to the driver", 
                "WPA: Failed to get random data for ANonce",
                "TDLS: TPK-TK for the peer", 
                "has already been configrued to the driver - do not reconfigure",
                "WNM: Ignore WNM-Sleep Mode Response frame since WNM-Sleep Mode operation has not been requested",
                "WPA: Not reinstalling already in-use GTK to the driver",
                "FT: Reassociation has already been completed for this FT protocol instance - ignore unexpected retransmission",
                "CodyLentPatch3Placeholder",
                "CodyLentPatch4Placeholder"]

def main(command):
    if command == "":
        print "Must supply wpa_supplicant command"
        return 0
    print command
        
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    for line in iter(proc.stdout.readline, ''):
        if any(naughty_phrase in line for naughty_phrase in naughty_list):
            #Found a bad printout
            print "Found a bad one!"
            
if __name__ == "__main__":
    file_name = basename(__file__)
    command = ""
    for token in argv:
        if token != file_name:
            command += token + " "
            
    if "-ddd" not in command:
        command += "-ddd"

    main(command)

#!/usr/bin/env pyt

import subprocess
import unittest
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

def main(command, test=False, source=None):
    if command == "":
        print "Must supply wpa_supplicant command"
        return 0
    print command

    if not test or source is None:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        source = iter(proc.stdout.readline, '')

    ret = 0

    for line in source:
        if any(naughty_phrase in line for naughty_phrase in naughty_list):
            #Found a bad printout
            print "Found a bad one!"
            ret += 1

    return ret


class TestSearch(unittest.TestCase):
    def testMain(self):
        test1_source = ["FT: Do not re-install same PTK to the driver", 
            "WPA: Failed to get random data for ANonce",
            "TDLS: TPK-TK for the peer", 
            "has already been configrued to the driver - do not reconfigure",
            "WNM: Ignore WNM-Sleep Mode Response frame since WNM-Sleep Mode operation has not been requested",
            "WPA: Not reinstalling already in-use GTK to the driver",
            "FT: Reassociation has already been completed for this FT protocol instance - ignore unexpected retransmission",
            "CodyLentPatch3Placeholder",
            "CodyLentPatch4Placeholder"] 
        self.assertEqual(main("test_tool", test=True, source=test1_source), 9)

        test2_source = ["FT: Do not re-install same PTK to the driver", "Nothing", "Still nothing"]
        self.assertEqual(main("test_tool", test=True, source=test2_source), 1)

        test3_source = ["Nothing", "Other nothing", "this isn't anything"]
        self.assertEqual(main("test_tool", test=True, source=test3_source), 0)

            
if __name__ == "__main__":
    file_name = basename(__file__)
    command = ""
    for token in argv:
        if token != file_name:
            command += token + " "

    if command == "test_tool":
        unittest.main()

    else:     
        if "-ddd" not in command:
            command += "-ddd"

        main(command)
#!/usr/bin/env pyt

import subprocess
from sys import stdin, argv
from os.path import basename

naughty_list = ["FT: Do not re-install same PTK to the driver", 
                "oh, another one"]

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
        else:
            print "Read good line"
if __name__ == "__main__":
    file_name = basename(__file__)
    command = ""
    for token in argv:
        if token != file_name:
            command += token + " "

    main(command)

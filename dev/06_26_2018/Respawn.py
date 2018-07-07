# Universal Power System Controller
# USAID Middle East Water Security Initiative
#
# Developed by: Nathan Webster
# Primary Investigator: Nathan Johnson
#
# Version History (mm_dd_yyyy)
# 1.00 07_13_2018_NW
#
######################################################
#!/usr/bin/python3

from subprocess import Popen
import sys

filename = sys.argv[1]

while True:
    print("\nStarting "+filename)
    p = Popen("python3 "+ filename,shell=True)
    p.wait()
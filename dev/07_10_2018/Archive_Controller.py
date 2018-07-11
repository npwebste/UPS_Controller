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
# Import Libraries
import sqlite3
import sched
import time
import zipfile
import os
from datetime import datetime
import Parameters
from UPS_Error import *

def Archive_Controller_Main(arg):

    # Setup Archive scheduler
    Archive_Sched = sched.scheduler(time.time, time.sleep)

    while True:
        # Schedule the SQL controller and run
        Archive_Sched.enter(Parameters.Archive_Controller_Interval, 1, Archive_Controller, ("",))
        Archive_Sched.run()

def Archive_Controller(arg):
    try:
        conn = sqlite3.connect('UPS_DB.db')
        c = conn.cursor()
        csvdata = c.execute("SELECT * from UPS_DB")

    except:
        UPS_Error('CSV Error')

    with open('UPS_CSV.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ['Column1', 'Column2', 'Column3', 'Column4', 'Column5', 'Column6', 'Column7', 'Column8', 'Column9'])
        writer.writerows(csvdata)
    csvfile.close()

    # Create archive directory for current time
    Current_time = datetime.now()
    directory = '/home/pi/datalogger/Archive/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create archive
    zf_name = f'{Current_time}_Archive'
    zf = zipfile.Zipfile(zf_name,'w')

    # Write log to zip file
    try:
        with zipfile.Zipfile(zf_name,'w') as zf:
            zf.write('UPS_DB.sql', zipfile.ZIP_STORED)
            zf.write('UPS_Error.log', zipfile.ZIP_STORED)
            zf.write('UPS_DB.csv', zipfile.ZIP_STORED)
    except:
        UPS_Error('Arhive Error')

    try:
        os.remove('UPS_Error.log')
        os.remove('UPS_DB.csv')

        c.execute('DELETE FROM UPS_DB WHERE ')

        conn.close()
    except:
        UPS_Error('Archive Delete'


    # Write sql database to zip file

    # Write csv file to zip file

    # Delete log file

    # Delete sql database older than one week

    # Delete csv file


    Currenttime = datetime.now()
    try:
        conn = sqlite3.connect('UPS_DB.db')
        c = conn.cursor()
        c.execute("INSERT INTO UPS_DB(Date,Solar_Voltage, DC_Link_Voltage, VFD_Freq, VFD_Volt, VFD_Amps, VFD_Power, VFD_BusVolt, VFD_Temp) VALUES(?,?,?,?,?,?,?,?,?)",(Currenttime, Solar_Voltage,DC_Link_Voltage,VFD_Freq,VFD_Volt,VFD_Amps,VFD_Power,VFD_BusVolt,VFD_Temp))
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("SQL write failed")
        raise e
    conn.close()
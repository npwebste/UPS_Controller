# ©2018 The Arizona Board of Regents for and on behalf of Arizona State University and the Laboratory for Energy And Power Solutions, All Rights Reserved.
#
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

# VFD register values for reading and writing
reg = {
    "WriteFunc":{
        "Frequency_Set":269,
		"Frequency_Max":267,
		"Frequency_Min":268,
		"Frequency_Acc":270,
        "Motor_Start_Stop":8192
        },
    "ReadFunc":{
        "Output_Frequency":4096,
        "Output_Voltage":4097,
        "Output_Current":4098,
        "Output_Speed":4119,
        "Output_Power":4120,#4106
        "Bus_Voltage":4100,
        "Frequency_Set":269,
        "Temperature":4103
        }
    }

'''
VFD modbus value multipliers
Freq = 100
Current = 100
Voltage = Actual
Power = 10
'''
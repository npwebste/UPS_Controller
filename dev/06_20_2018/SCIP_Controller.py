# Universal Power Supply Controller
# USAID Middle East Water Security Initiative
#
# Developed by: Nathan Webster
# Primary Investigator: Nathan Johnson
#
# Version History (mm_dd_yyyy)
# 1.00 03_24_2018_NW
#
######################################################
# Import Libraries
import Parameters
from PySCIPOpt import *


def SCIP_Controller(Solar_Power):
    SCIP_Power, SCIP_Freq = UPS_SCIP_Call()

    return SCIP_Power, SCIP_Freq

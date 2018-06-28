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
import logging
import inspect

def UPS_Error(ErrorCode):
    logger = function_logger(logging.DEBUG)
    if (ErrorCode == 'Error_VFD_Freq'):
        print('VFD frequency set above maximum, shutting down motor')
    elif ErrorCode == 'Error_VFD_Volt':
        print('VFD votlage set above maximum, shutting down motor')
    elif ErrorCode == 'Error_VFD_Amps':
        print('VFD current set above maximum, shutting down motor')
    elif ErrorCode == 'Error_VFD_Power':
        print('VFD power set above maximum, shutting down motor')
    elif ErrorCode == 'Error_VFD_BusVolt':
        print('VFD bus voltage set above maximum, shutting down motor')
    elif ErrorCode == 'Error_VFD_Temp':
        print('VFD temperature set above maximum, shutting down motor')
    elif ErrorCode == 'Error_Solar_Voltage':
        print('Solar voltage set above maximum, shutting down converter and motor')
    elif ErrorCode == 'Error_DC_Link_Voltage':
        print('DC link voltage set above maximum, shutting down converter and motor')
        logger.warn('DC link voltage set above maximum, shutting down converter and motor')
    elif ErrorCode == 'Error_Voltage_Measurement':
        print('Incorrect voltage measurement input')
    elif ErrorCode == 'Error_Transfer_Switch':
        print('Incorrect transfer switch input')
    elif ErrorCode == 'Error_VFD_Power':
        print('Incorrect power calculation')
    elif ErrorCode == 'Error_Duty_Cycle':
        print('Incorrect power calculation')
    logging.shutdown()


def function_logger(file_level):
    function_name = inspect.stack()[1][3]
    logger = logging.getLogger(function_name)
    logger.setLevel(logging.DEBUG) #By default, logs all messages

    fh = logging.FileHandler("{0}.log".format(function_name))
    fh.setLevel(file_level)
    fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
    fh.setFormatter(fh_format)
    logger.addHandler(fh)

    return logger
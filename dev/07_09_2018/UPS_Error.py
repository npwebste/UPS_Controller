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
import logging
import inspect

# Function for printing errors messages and calling logger ]
def UPS_Error(ErrorCode):
    logger = function_logger(logging.DEBUG)
    if (ErrorCode == 'Error_VFD_Freq'):
        print('VFD frequency set above maximum, shutting down motor')
        logger.warn('VFD frequency set above maximum, shutting down motor')

    elif ErrorCode == 'Error_VFD_Volt':
        print('VFD votlage set above maximum, shutting down motor')
        logger.warn('VFD votlage set above maximum, shutting down motor')

    elif ErrorCode == 'Error_VFD_Amps':
        print('VFD current set above maximum, shutting down motor')
        logger.warn('VFD current set above maximum, shutting down motor')

    elif ErrorCode == 'Error_VFD_Power':
        print('VFD power set above maximum, shutting down motor')
        logger.warn('VFD power set above maximum, shutting down motor')

    elif ErrorCode == 'Error_VFD_BusVolt':
        print('VFD bus voltage set above maximum, shutting down motor')
        logger.warn('VFD bus voltage set above maximum, shutting down motor')

    elif ErrorCode == 'Error_VFD_Temp':
        print('VFD temperature set above maximum, shutting down motor')
        logger.warn('VFD temperature set above maximum, shutting down motor')

    elif ErrorCode == 'Error_Solar_Voltage':
        print('Solar voltage set above maximum, shutting down motor and opening solar relay')
        logger.warn('Solar voltage set above maximum, shutting down motor and opening solar relay')

    elif ErrorCode == 'Error_DC_Link_Voltage':
        print('DC link voltage set above maximum, shutting down motor and opening solar relay')
        logger.warn('DC link voltage set above maximum, shutting down motor and opening solar relay')

    elif ErrorCode == 'Error_Voltage_Measurement':
        print('Error reading voltage measurement')
        logger.warn('Error reading voltage measurement')

    elif ErrorCode == 'Error_Transfer_Switch':
        print('Invalid transfer switch command')
        logger.warn('Invalid transfer switch command')

    elif ErrorCode == 'Error_DC_Relay':
        print('Invalid DC relay command')
        logger.warn('Invalid DC relay command')

    elif ErrorCode == 'Error_VFD_Power':
        print('Invalid power value calculated')
        logger.warn('Invalid power value calculated')

    elif ErrorCode == 'Error_Duty_Cycle':
        print('Invalid duty cycle value calculated')
        logger.warn('Invalid duty cycle value calculated')

    elif ErrorCode == 'Error_Solar_Voltage_Relay':
        print('Solar voltage out of accecptable range, cannot turn on solar relay')
        logger.warn('Solar voltage out of accecptable range, cannot turn on solar relay')

    logging.shutdown()

# Logger function for writing messages to error log file
def function_logger(file_level):
    function_name = inspect.stack()
    logger = logging.getLogger(function_name)
    logger.setLevel(logging.DEBUG) #By default, logs all messages

    fh = logging.FileHandler("{0}.log".format(function_name))
    fh.setLevel(file_level)
    fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
    fh.setFormatter(fh_format)
    logger.addHandler(fh)

    return logger
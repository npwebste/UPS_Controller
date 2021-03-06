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
import sys
#global logger
#logger = function_logger(logging.DEBUG)

# Function for printing errors messages and calling logger ]
def UPS_Messages(MessageCode):
    global logger
    logger = function_logger(logging.DEBUG)
    if (MessageCode == 'Error_VFD_Freq'):
        print('VFD frequency set above maximum, shutting down motor')
        logger.warn('VFD frequency set above maximum, shutting down motor')

    elif MessageCode == 'Error_VFD_Volt':
        print('VFD votlage set above maximum, shutting down motor')
        logger.warn('VFD votlage set above maximum, shutting down motor')

    elif MessageCode == 'Error_VFD_Amps':
        print('VFD current set above maximum, shutting down motor')
        logger.warn('VFD current set above maximum, shutting down motor')

    elif MessageCode == 'Error_VFD_Power':
        print('VFD power set above maximum, shutting down motor')
        logger.warn('VFD power set above maximum, shutting down motor')

    elif MessageCode == 'Error_VFD_BusVolt':
        print('VFD bus voltage set above maximum, shutting down motor')
        logger.warn('VFD bus voltage set above maximum, shutting down motor')

    elif MessageCode == 'Error_VFD_Temp':
        print('VFD temperature set above maximum, shutting down motor')
        logger.warn('VFD temperature set above maximum, shutting down motor')

    elif MessageCode == 'Error_Solar_Voltage':
        print('Solar voltage set above maximum, shutting down motor and opening solar relay')
        logger.warn('Solar voltage set above maximum, shutting down motor and opening solar relay')

    elif MessageCode == 'Error_DC_Link_Voltage':
        print('DC link voltage set above maximum, shutting down motor and opening solar relay')
        logger.warn('DC link voltage set above maximum, shutting down motor and opening solar relay')

    elif MessageCode == 'Error_Voltage_Measurement':
        print('Error reading voltage measurement')
        logger.warn('Error reading voltage measurement')

    elif MessageCode == 'Error_Transfer_Switch':
        print('Invalid transfer switch command')
        logger.warn('Invalid transfer switch command')

    elif MessageCode == 'Error_DC_Relay':
        print('Invalid DC relay command')
        logger.warn('Invalid DC relay command')

    elif MessageCode == 'Error_VFD_Power':
        print('Invalid power value calculated')
        logger.warn('Invalid power value calculated')

    elif MessageCode == 'Error_Duty_Cycle':
        print('Invalid duty cycle value calculated')
        logger.warn('Invalid duty cycle value calculated')

    elif MessageCode == 'Error_Solar_Voltage_Relay':
        print('Solar voltage out of accecptable range, cannot turn on solar relay')
        logger.warn('Solar voltage out of accecptable range, cannot turn on solar relay')

    elif MessageCode == 'Error Archive':
        print('Could not archive database')
        logger.warn('Could not archive database')

    elif MessageCode == 'Error Archive Delete':
        print('Could not update SQL or delete CSV and log file')
        logger.warn('Could not update SQL or delete CSV and log file')

    elif MessageCode == 'Error SQL Connection':
        print('Could not connect to SQL database')
        logger.warn('Could not connect to SQL database')

    elif MessageCode == 'Error SQL Create':
        print('Could not creat SQL database')
        logger.warn('Could not connect to SQL database')

    #print(logger)
    #logging.Handler.close(self)
    logging.shutdown()
    #logger.Handler.close()
    #print(logger)
    #logger.shutdown()
    #handlers = logger.handlers[:]
    #for handler in handlers:
    #    handler.close()
    #    logger.removeHandler(handler)
    #logging.Handler.close()

# Logger function for writing messages to error log file
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
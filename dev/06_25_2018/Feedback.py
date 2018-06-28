#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from ADS1256_definitions import *
from pipyadc import ADS1256

EXT2, EXT3, EXT4 = POS_AIN2|NEG_AINCOM, POS_AIN3|NEG_AINCOM, POS_AIN4|NEG_AINCOM
EXT5, EXT6, EXT7 = POS_AIN5|NEG_AINCOM, POS_AIN6|NEG_AINCOM, POS_AIN7|NEG_AINCOM

def do_measurement():
    ### STEP 1: Initialise ADC object:
    ads = ADS1256()

    ### STEP 2: Gain and offset self-calibration:
    ads.cal_self()

    ### STEP 3: Get data:
    adsread = ads.read_oneshot(EXT3)
    voltage = adsread * ads.v_per_digit
    return voltage
/*
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
 */


#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

void PWM_Setup (void){
	if(wiringPiSetup()==-1){
	printf("Could not initialize");
	exit(1);
	}
}

void PWM_Pin_Mode(int Pin){
	pinMode(Pin,PWM_OUTPUT);
	printf("Pin = %d, Output = %d\n", Pin,PWM_OUTPUT);
}

void Pin_Mode(int Pin){
	pinMode(Pin,OUTPUT);
	printf("Pin = %d, Output = %d\n", Pin,OUTPUT);
}

void PWM_Set_Mode(){
	pwmSetMode(PWM_MODE_MS);
    	printf("Mode = %d \n",PWM_MODE_MS);
}

void PWM_Set_Clock(int Divisor){
	pwmSetClock(Divisor);
	printf("Divisor = %d \n",Divisor);
}

void PWM_Set_Range(unsigned int Range){
	pwmSetRange(Range);
	printf("Range = %d \n",Range);	
}
void PWM_Write(int Pin, int Value){
	pwmWrite(Pin,Value);
	//printf("Pin = %d, Value = %d",Pin,Value);
}

void Digital_Write(int Pin, int Value){
	digitalWrite(Pin,Value);
	//printf("Pin = %d, Value = %d",Pin,Value);
}
/*
int main (void)
{

  printf ("Raspberry Pi wiringPi PWM test program\n") ;

  if (wiringPiSetup () == -1)
    exit (1) ;
  pinMode (1, PWM_OUTPUT) ;
  pwmSetMode(PWM_MODE_MS);
  pwmSetClock(2);
  pwmSetRange(96);
  pwmWrite (1,48) ;
    return 0 ;
}
*/
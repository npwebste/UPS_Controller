#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int PWM_Setup (void){
	wiringPiSetup()
	
}

int PWM_Pin_Mode(int Pin, char Output){
	
	
	
}

int PWM_Set_Mode(char Mode){
	
	
	
}

int PWM_Set_Clock(int Divisor){
	
	
	
}

int PWM_Set_Range(int Range){
	
	
	
}
int PWM_Write(int Pin, int Value){
	
	
	
}

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

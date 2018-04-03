#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int PWM_Setup (void){
	wiringPiSetup()
	
}

int PWM_Pin_Mode(int Pin, char Output){
	int PinMode;
	PinMode = pinMode(Pin,Output);
	printf("Pin = %d, Output = %s \n", Pin, Output);
	return Pin_Mode;	
}

int PWM_Set_Mode(char Mode){
	int SetMode;
	SetMode = pwmSetMode(Mode);
    printf("Mode = %s \n",Mode);
	return SetMode;	
}

int PWM_Set_Clock(int Divisor){
	int SetClock;
	SetClock = pwmSetClock(Divisor);
	printf("Divisor = %d \n",Divisor);
}

int PWM_Set_Range(int Range){
	int SetRange;
	SetRange = pwmSetRange(Range);
	printf("Range = %d \n",Range);	
	return SetRange;
}
int PWM_Write(int Pin, int Value){
	int PWMWrite;
	PWMWrite = pwmWrite(Pin,Value);
	printf("Pin = %d, Value = %d",Pin,Value);
	return PWMWrite;
}

int Digital_Write(int Pin, int Value){
	int DigitalWrite;
	DigitalWrite = digitalWrite(Pin,Value);
	printf("Pin = %d, Value = %d",Pin,Value);
	return DigitalWrite;
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
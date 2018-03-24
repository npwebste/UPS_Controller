#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <unistd.h>

#ifdef WIN32
#include <winsock2.h>
#else
#include <arpa/inet.h>
#endif

#include "modbus.h"

modbus_t	*ctx;
uint16_t        *readval;

int      	readVFDRegister     	(int);
int		writeVFDRegister	(int, int);
//int VFDInit(char *Device, int Baud, char Parity, int Data, int Stop, int Server_ID)
int VFDInit(char *Device, int Baud, int Data, int Stop, int Server_ID)
{
	int			rc;
	int			i = 0;
	int			flag = 0;
//	int			addr;
	int			nb;
	int 			rt;

	/* RTU */
//	ctx = modbus_new_tcp(address, port);
	ctx = modbus_new_rtu(Device, Baud, 'N', Data, Stop);
	//ctx = modbus_new_rtu("/dev/ttyUSB0", 19200, 'N', 8, 1);
        rt = modbus_set_slave(ctx, Server_ID);
	fprintf(stderr, "Set Slave: %d \n",rt);
	
	printf("Device = %s, Baud = %d,Data = %d, Stop = %d, ID = %d \n", Device, Baud, Data, Stop, Server_ID);
	printf("Connect Return = %d \n",modbus_connect(ctx));
	//modbus_flush(ctx);
	while(i < 4){
	
	if (-1 == modbus_connect(ctx))
	{	

		if(flag ==  1 && i == 3)
		{	fprintf(stderr, "Connection failed: %s\n",
			modbus_strerror(errno));
			printf("modbus failed\n");
			//printf("Device = %s, Baud = %d, Stop = %d, ID = %d \n", Device, Baud, Stop, Server_ID);
			//printf("Device = %s, Baud = %d, Partiy = %c, Stop = %d, ID = %d \n", Device, Baud, Parity, Stop, Server_ID);
			//printf("Connect Return = %s \n",ctx);
			return -1;
		}
		flag = 1;
		sleep(1);
		//return -1;
	}
	else 
	    break;
	i++;
	printf("Success?");
	}
}


void VFDClose(void)
{
	if (0 != ctx)
	{
		modbus_close(ctx);
		modbus_free(ctx);
		printf("Connetion Closed \n");
	}
}


//////////////////////////////////////////////////////////


int writeVFDRegister(int addr1, int value)
{
	int			rc;
	//int			addr1;
	//int addr3;
	//int value1;
	
	//rc = modbus_write_register(ctx, 8192, 1);
	rc = modbus_write_register(ctx, addr1, value);
	//rc = modbus_write_register(ctx, addr3, value1);
	printf("%d, %d, %d, 0x%X %d \n",modbus_connect(ctx), addr1, value, value,rc);
	
	if (-1 == rc)
	{
		fprintf(stderr, "Write Register failed: %s\n", modbus_strerror(errno));
    }
	else{
		return -1;
	}
	return rc;
}

int readVFDRegister(int addr2)
{
	int		result;
	int			rc;
	//int			addr2;
	const int	nb = 1;
	
	//uint16_t readval;

	rc = modbus_read_registers(ctx, addr2,nb, readval);
	
	if (-1 == rc)
	{
		fprintf(stderr, "Read Register failed: %s\n", modbus_strerror(errno));
    }
	else{
		return -1;
	}
	return rc;
}

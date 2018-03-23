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

int      	readVFDRegister     	(int, SunSpecField);
int			writeVFDRegister		(int, SunSpecField, uint16);

int VFDInit(char *Device, int Baud, char *Parity, int Data, int Stop, int Server_ID)
{
	int			rc;
	int			i = 0;
	int			flag = 0;
//	int			addr;
	int			nb;

	/* RTU */
//	ctx = modbus_new_tcp(address, port);
	ctx = modbus_new_rtu(Device, Baud, Parity, Data, Stop);
	//ctx = modbus_new_rtu("/dev/ttyUSB0", 19200, 'N', 8, 1);
    //modbus_set_slave(ctx, Server_ID);

	while(i < 4){
	
	if (-1 == modbus_connect(ctx))
	{	

		if(flag ==  1 && i == 3)
		{	fprintf(stderr, "Connection failed: %s\n",
			modbus_strerror(errno));
			printf("modbus failed\n");
			return -1;
		}
		flag = 1;
		sleep(1);
		return -1;
	}
	else 
	    break;
	i++;
	}
}


void VFDClose(void)
{
	if (0 != ctx)
	{
		modbus_close(ctx);
		modbus_free(ctx);
	}
}


//////////////////////////////////////////////////////////


int writeVFDRegister(int addr, uint16 value)
{
	int			rc;
	int			addr;
	
	rc = modbus_write_register(ctx, addr, value);
	
	if (-1 == rc)
	{
		fprintf(stderr, "Write Register failed: %s\n", modbus_strerror(errno));
    }
	else{
		return -1;
	}
	return rc;
}

int readVFDRegister(int addr)
{
	uint16		result;
	int			rc;
	int			addr;
	const int	nb = 1;
	
	uint16 readval[2];
	rc = modbus_read_registers(ctx, addr,nb, readval);
	
	if (-1 == rc)
	{
		fprintf(stderr, "Write Register failed: %s\n", modbus_strerror(errno));
    }
	else{
		return -1;
	}
	return rc;
}

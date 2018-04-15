import ads1256       # import this lib                             

gain = 1			 # ADC's Gain parameter
sps = 25		 # ADC's SPS parameter



# Initialize the ADC using the parameters
ads1256.start(str(gain),str(sps))  

# Fill the first list with all the ADC's absolute channel values
ChannelValue = ads1256.read_channel(0)
                
	# Fill the second list  with the voltage values
ChannelValueVolts = (((ChannelValue * 100) /167.0)/int(gain))/1000000.0   
ChannelValueVolts2 = (((ChannelValue)/int(gain))*3.3) /16777216

print ChannelValue

print ChannelValueVolts

print ChannelValueVolts2


# Print a new line
print ("\n");							   
    

# Stop the use of the ADC
ads1256.stop()
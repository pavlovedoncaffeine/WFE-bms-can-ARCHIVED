# To-Do

# pyCAN: Edit canbus you're reading from (ask Alex for the correct Bus or check once connected to the VN1610) 
#		 Fill in code for checking DTC codes against the *.csv file
#		 Fill in code for checking BMU_cell voltages against the voltages set on the Bloomy (in pyLAN)
#		 Fill in code for checking BMU-cell temps are within expected range
#		 Fill in code for checking that PDU fuses aren't blown

# pyUART: Edit the socket you're sending the reset signal (check what the reset signal should be) - Alex?

# pyLAN: Create a connection to the Bloomy
#		 Set voltages to nominal 3.7V per cell for all 1-12 cell channels
#		 Set voltage on a per channel basis to nominal, under and overvolt values
# 		 

# main: Compare set voltage and cell channel with the CAN and ensure the correct cell voltage is being read back
#		Ensure cell temps are within expected range
#		Ensure all fuses are not blown
#		Change cell channel voltage to under and overvolt scenarios each, and ensure DTC codes are displayed
#		Reset bloomy after each cell volt check; repeat for 12 cell channels


# Waterloo Forumla Electric 

# Main function to run python scripts to use 
#	the CANbus, the LAN for the Bloomy (battery simulator) and UART for reset the 12-cell BMU

import sys
import csv
import pprint

import pyCAN	#CAN bus functions for DTC, Cell Voltages, Cell Temps, and PDU status (fuses?)
import pyLAN	#LAN functions to control the Bloomy Battery Simulator
import pyUART	#UART function to reset BMU (in progress)






def main():


if __name__ == '__main__':
	main()
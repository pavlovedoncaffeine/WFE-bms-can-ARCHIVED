# Waterloo Forumla Electric 

# BMU Main Testing Script (all hardware and software tests + safety tests)
# Check for undervolt and overvolt scenarios for each cell after the Bloomy's cell is set accordingly
# Check for relevant BMU_DTC codes and compare BMU_CellVoltage against Bloomy's set voltages
# Check to ensure BMU's cell temps are within an expected range
# Check to ensure fuses aren't blown (DTC code check)
# 

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
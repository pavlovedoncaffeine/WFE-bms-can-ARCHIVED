# Waterloo Forumla Electric 

# functions for reading and checking CAN data against set values on the Bloomy (LAN)

import sys 
import csv
import math
import cantools
from pprint import pprint
import can

#------------------------------------------------------------------------------------------------

# db is an object of class cantools.database.can.Database()
# This contains the structure of all messages and their corresponding signals, signal names and relevant data as well
db = cantools.database.load_file('2018CAR.dbc')

#------------------------------------------------------------------------------------------------

#Specify the can bus in use either virtual (Vcan0) or vector (for the VN1610 used by the WFE team)
#can_bus = can.interface.Bus(bustype='vector', appname = 'CANalyzer', channel = 0, bitrate=250000)
#can_bus = can.interface.Bus('vcan0', bustype='socketcan') 
can_bus = can.interface.Bus('testing', bustype='virtual')

#------------------------------------------------------------------------------------------------

filename = 'DTC.csv'
DTCFile = open(filename, newline='\n')
readDTC = csv.reader(DTCFile) #readDTC is a 2D array with all CSV elements and can be iterated through
#DTCFile.close() #close after the entire script is done?

#------------------------------------------------------------------------------------------------
#cantools.database.can.Message class objects for both DTC codes and for Cell voltages
DTC_msg = db.get_message_by_name("BMU_DTC")
volts_msg = db.get_message_by_name("BMU_CellVoltage")
temp_msg = db.get_message_by_name("BMU_CellTemp")

#dictionaries for BMU_DTC and for BMU_CellVoltage, BMU_CellTemp and PDU_ChannelStatus
dtc_dict = {"empty" : 0}
volts_dict = {"empty" : 0} 
temp_dict = {"empty" : 0}

#------------------------------------------------------------------------------------------------

#Listing all functions below:


#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

# dtc_dict contains signals for the BMU_DTC message. If dtc_dict is empty there's no DTC code on the CAN.
def checkDTC():
	try:
		if ((len(dtc_dict)) <= 0 or ('empty' in dtc_dict)):
			#dict empty, ie: no dtc codes
			for i in range(1,5):
				readDTC[i][5] = 'CellNumber'
				return false

		elif ('DTC_CODE' in dtc_dict):
			for i in range(1,5):
				# Compare DTC code in canbus with the DTC.csv file's first 4 lines
				if (dtc_dict["DTC_CODE"] == readDTC[i][0] and dtc_dict["DTC_Severity"] == readDTC[i][3]):
					readDTC[i][5] = dtc_dict["DTC_Data"] # change DTC 2D array with relevant cell number for 
					# return the dtc code and cell number related to the DTC code
					return dtc_dict["DTC_CODE"] ,dtc_dict["DTC_Data"]

				else:
					# dtc code on canbus unrelated to test script
					return false
		else:
			return false
	# find out why it says wrong indentation
	except:
		pprint("Could not check DTC dictionary for relevant dtc signals")
		return false
        



#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

# volts_dict contains signals for VoltageCellMuxSelect 
#   which in turn contain voltages for groups of 3 cells each

# checkVolts(mux_signals, cell_num, cell_v)
# return true/false
# mux_signals_required  - acceptable values: array of 4 conseq. mux values. Each element can
#						  only take values from 0 to 23 (24 mux values total) 
# cell_num 				- int: one of range(1..72) 
# cell_v				- float: expected voltage on given cell_num
def checkVolts(mux_signals_required, cell_num, cell_v):
	assert(len(mux_signals_required) == 4)
	assert(cell_num >= 1 and cell_num <= 72)
	assert(cell_v >= 0 and cell_v <= 5.0) 

	try:
		if (len(volts_dict) <= 0 or ('empty' in volts_dict)):
			return false 				#dict empty, ie: no dtc codes
		else:
			#for each mux value, check volts on each of the 3 signals
			#for mux_sig in mux_signals_required:
			for mux_sig in mux_signals_required:
				vCell_Signals = volts_dict.get(mux_sig) # get associated value to vCell_Signals

				#pprint(vCell_Signals) 	# debugging print
				pprint("Mux #:", mux_sig)
				pprint("Cell number expected:", cell_num)
				pprint("Cell numbers in mux starting at: {}\n", mux_sig*3 + 1)

				# iterate through vCell_Signals
				for i in range(0, 3):
					pprint(vCell_Signals[i])
					# tolerance set at 10% of cell voltage for now
					if (((i+1+mux_sig*3) == cell_num) and (math.isclose(vCell_Signals[i], cell_v, abs_tol = 0.03))):
						pprint("Cell voltage of cell %d, as expected", cell_num)
					elif (math.isclose(vCell_Signals[i], 3.7, abs_tol = 0.03)):
						pprint("Cell at nominal voltage as expected")
					else:
						raise Exception("ERROR: Cell %d at incorrect voltage", (i+1+mux_sig*3))
						exit(99) #error 99: cell incorrect voltage reported; script ends
		return true
	finally:
		return false



# checkAllVolts(cell_v) 
# cell_v				- float: expected voltage on all cells
def checkAllVolts(cell_v):
	assert(cell_v >= 0 and cell_v <= 5.0) 

	try:
		if (len(volts_dict) <= 0 or ('empty' in volts_dict)):
			return false 				#dict empty, ie: no dtc codes
		else:
			#for each mux value, check volts on each of the 3 signals
			#for all mux_sig:
			for mux_sig in volts_dict.keys():
				vCell_Signals = volts_dict.get(mux_sig) # get associated value to vCell_Signals

				#pprint(vCell_Signals) 	# debugging print
				pprint("Mux #:", mux_sig)

				for vcell_sig in vCell_Signals:
					if (math.isclose(vCell_Signals[vcell_sig], cell_v, abs_tol = 0.03)):
						# change debug print statement to show which cell we're talking about. 
						# ensures you don't have a wall of text for 72 lines saying the same
						# shit
						pprint("Cell at nominal voltage as expected")
					else:
						raise Exception("ERROR: Cell at incorrect voltage")
						exit(99) #error 99: cell incorrect voltage reported; script ends
				return true
	finally:
		return false



#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

#temp_dict contains signals for a muxxed TempCellxx 
def checkTemps(t_low, t_high):
	try:
		if (len(temp_dict) <= 0 or ('empty' in temp_dict)):
			return false 				#dict empty, ie: no dtc codes
		else:
			#for each mux value, check volts on each of the 3 signals
			#for all mux_sig:
			for mux_sig in temp_dict.keys():
				tCell_Signals = temp_dict.get(mux_sig) # get associated value to vCell_Signals

				#pprint(vCell_Signals) # debugging print
				pprint("Mux #:", mux_sig)

				for tcell_sig in tCell_Signals:
					if (tcell_sig >= t_low and tcell_sig <= t_high):
						# change debug print statement to show which cell we're talking about. 
						# ensures you don't have a wall of text for 72 lines saying the same
						# shit
						pprint("Cell temperature as expected")
					elif (tcell_sig < t_low):
						raise Exception("ERROR: Cell temperature below expected")
						exit(25) #error 25: cell undertemp script error
					elif (tcell_sig > t_high):
						raise Exception("ERROR: Cell temperature above expected")
						exit(22) #error 22: cell overtemp script error
				return true
	finally:
		return false


#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

#prints all DTC.csv cells to ensure all data is available -- debugging function mostly 
def print_all_DTC():
	try:
		for row in readDTC:
			for cell in row:
				sys.stdout.write("{}\t\t", cell)
			print()
	except csv.Error as e:
		sys.exit('File: {}, line {}\nError: {}\n'.format(filename, readDTC.line_num, e))

#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

# Reads incoming CAN messages and decodes to any of the following:
# BMU_DTC
# BMU_CellVoltage
# BMU_CellTemp
# Returns true if the message received matches frame_id of any of the above, else returns false

def read_CAN_msg():
	msg = can_bus.recv() #receive a message from the CAN bus
	#use arbitration_id to compare to frame_id of messages and decode after matching IDs
	#frame id for BMU_DTC = 0xff01
	if (msg.arbitration_id == DTC_msg.frame_id): 
		pprint("Recevied msg.frame_id matches expected BMU_DTC's frame id \n")
		dtc_dict = db.decode_message(msg.arbitration_id, msg.data) #hopefully decodes received message to a {signal name : values} dictionary
		#checkDTC()
		return 1
	#frame id for BMU_CellVoltage = 0x18800401
	elif (msg.arbitration_id == volts_msg.frame_id):
		print("Recevied msg.frame_id matches expected BMU_CellVoltage's frame id \n")
		# dictionary with mux signal key-value pairs
		volts_dict = db.decode_message(msg.arbitration_id, msg.data) #rewrite volts_msg with incoming data
		#checkVolts()
		return 2
	#frame id for BMU_CellTemp = 0x18c00401
	elif (msg.arbitration_id == temp_msg.frame_id):
		print("Recevied msg.frame_id matches expected BMU_CellTemp's frame id \n")
		# dictionary with mux signal key-value pairs
		temp_dict = db.decode_message(msg.arbitration_id, msg.data)
		#checkTemps()
		return 3
	else:
		print("Recevied message didn't match BMU_DTC or BMU_CellVoltage or BMU_CellTemp \n")
		return 0

#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo


# The following lines acn be used for module testing:
# i)    print_all_DTC()
# ii)   read_CAN_msg()


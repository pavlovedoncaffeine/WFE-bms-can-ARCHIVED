# Waterloo Forumla Electric 

# functions for reading and checking CAN data against set values on the Bloomy (LAN)

import sys 
import csv
import cantools
import pprint
import can

#------------------------------------------------------------------------------------------------

# db is an object of class cantools.database.can.Database()
# This contains the structure of all messages and their corresponding signals, signal names and relevant data as well
db = cantools.database.load_file('2018CAR.dbc')
# db complains about the masked frame id of "ChargeCart_ButtonEvents" and "TempCoolantRight" and overwrites TempCoolantRight

#------------------------------------------------------------------------------------------------

#Specify the can bus in use either virtual (Vcan0) or vector (for the VN1610 used by the WFE team)
#can_bus = can.interface.Bus(bustype='vector', appname = 'CANalyzer', channel = 0, bitrate=250000)
#can_bus = can.interface.Bus('vcan0', bustype='socketcan') 

#------------------------------------------------------------------------------------------------

#printobj = pprint.PrettyPrinter(indent=6)
filename = "DTC.csv"
DTCFile = open(filename, newline='\n')
readDTC = csv.reader(DTCfile) #readDTC is a 2D array with all CSV elements and can be iterated through
DTCfile.close()

#------------------------------------------------------------------------------------------------

#dictionaries for BMU_DTC and for BMU_CellVoltage
dtc_dict = {"empty" : 0}
volts_dict = {"empty" : 0} 
temp_dict = {"empty" : 0}
pdu_dict = {"empty" : 0} 

#cantools.database.can.Message class objects for both DTC codes and for Cell voltages
DTC_msg = get_message_by_name("BMU_DTC")
volts_msg = get_message_by_name("BMU_CellVoltage")
temp_msg = get_message_by_name("BMU_CellTemp")
pdu_msg = get_message_by_name("PDU_ChannelStatus")
#------------------------------------------------------------------------------------------------

#Listing all functions below:

#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

# dtc_dict contains signals for the BMU_DTC message. If dtc_dict is empty there's no DTC code on the CAN.
def checkDTC():


# volts_dict contains signals for VoltageCellMuxSelect 
#   which in turn contain voltages for groups of 3 cells each
def checkVolts():


#temp_dict contains signals for TempCellMuxSelect which in turn contains temps for groups of 3 cells each
def checkTemps(): 


#pdu_dict contains signals for blown fuses etc (I think?)
def checkPDUStatus():


#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

#prints all DTC.csv cells to ensure all data is available 
def print_all_DTC():
    try:
        for row in readDTC:
            for cell in row:
                sys.stdout.write(cell + "\t\t"),
            print()
            #prinntobj.pprint(readDTC) Didn't work when trying to print a whole csv file
    except csv.Error as e:
        sys.exit('File: {}, line {}\nError: {}\n'.format(filename, readDTC.line_num, e))

#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

# Reads incoming CAN messages and decodes to any of the following:
# BMU_DTC
# BMU_CellVoltage
# BMU_CellTemp
# PDU_ChannelStatus

def read_CAN_msg():
    msg = can_bus.recv()

    #frame id for BMU_DTC = 0xff01
    if (msg.frame_id == DTC_msg.frame_id): 
        print("Recevied msg.frame_id matches expected BMU_DTC's frame id \n")
        dtc_dict = db.decode_message(msg.frame_id, msg.data) #hopefully decodes received message to a {signal name : values} dictionary
        checkDTC()

    #frame id for BMU_CellVoltage = 0x18800401
    else if (msg.frame_id == volts_msg.frame_id):
        print("Recevied msg.frame_id matches expected BMU_CellVoltage's frame id \n")
        volts_dict = db.decode_message(msg.frame_id, msg.data)
        checkVolts()

    #frame id for BMU_CellTemp = 0x18c00401
    else if (msg.frame_id == temp_msg.frame_id):
        print("Recevied msg.frame_id matches expected BMU_CellTemp's frame id \n")
        temp_dict = db.decode_message(msg.frame_id, msg.data)
        checkTemps()

    #frame id for PDU_ChannelStatus = 0x6
    else if (msg.frame_id == pdu_msg.frame_id):
        print("Recevied msg.frame_id matches expected PDU_ChannelStatus's frame id \n")
        pdu_dict = db.decode_message(msg.frame_id, msg.data)
        checkPDUStatus()

    else:
        print("Recevied message didn't match BMU_DTC or BMU_CellVoltage or BMU_CellTemp \n")

#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo


# The following lines are used for module testing:
# i)    print_all_DTC()
# ii)   read_CAN_msg()


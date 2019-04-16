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
can_bus = can.interface.Bus('testing', bustype='virtual')

#------------------------------------------------------------------------------------------------

#printobj = pprint.PrettyPrinter(indent=6)
filename = 'DTC.csv'
DTCFile = open(filename, newline='\n')
readDTC = csv.reader(DTCFile) #readDTC is a 2D array with all CSV elements and can be iterated through
DTCFile.close()

#------------------------------------------------------------------------------------------------

#dictionaries for BMU_DTC and for BMU_CellVoltage
dtc_dict = {"empty" : 0}
volts_dict = {"empty" : 0} 
temp_dict = {"empty" : 0}
pdu_dict = {"empty" : 0} 

#cantools.database.can.Message class objects for both DTC codes and for Cell voltages
DTC_msg = db.get_message_by_name("BMU_DTC")
volts_msg = db.get_message_by_name("BMU_CellVoltage")
temp_msg = db.get_message_by_name("BMU_CellTemp")
pdu_msg = db.get_message_by_name("PDU_ChannelStatus")

#------------------------------------------------------------------------------------------------

#Listing all functions below:

#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

# dtc_dict contains signals for the BMU_DTC message. If dtc_dict is empty there's no DTC code on the CAN.
def checkDTC():
    try:
        if (len(dtc_dict) or ('empty' in dtc_dict) <= 0):
            #dict empty, ie: no dtc codes
            for i in range(1,5):
                readDTC[i][5] = 'CellNumber'
            return false

        elif ('DTC_CODE' in dtc_dict):
            for i in range(1,5):
                # Compare DTC code in canbus with the DTC.csv file's first 4 lines
                if (dtc_dict["DTC_CODE"] == readDTC[i][0] and dtc_dict["DTC_Severity"] == readDTC[i][3]):
                    readDTC[i][5] = dtc_dict["DTC_Data"] # change DTC 2D array with relevant cell number for 
                    
                    # below lines of code allow you to print the DTC code to terminal (irrelevant for tests)
                    # for cell in readDTC[i]:
                    #     sys.stduout.write(cell + "\t")
                    # print()

                    # return the dtc code and cell number related to the DTC code
                    return dtc_dict["DTC_CODE"] ,dtc_dict["DTC_Data"] 
                
                else:
                    # dtc code on canbus unrelated to test script
                    return false
        else:
            return false
    except:
        print("Could not check DTC dictionary for relevant dtc signals")
        return false
        



#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

# volts_dict contains signals for VoltageCellMuxSelect 
#   which in turn contain voltages for groups of 3 cells each
#def checkVolts():


#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

#temp_dict contains signals for TempCellMuxSelect which in turn contains temps for groups of 3 cells each
#def checkTemps():


#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo

#pdu_dict contains signals for blown fuses etc (I think?)
#def checkPDUStatus():


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
# Returns true if the message received matches frame_id of any of the above, else returns false

def read_CAN_msg():
    msg = can_bus.recv() #receive a message from the CAN bus
    #use arbitration_id to compare to frame_id of messages and decode after matching IDs

    #frame id for BMU_DTC = 0xff01
    if (msg.arbitration_id == DTC_msg.frame_id): 
        print("Recevied msg.frame_id matches expected BMU_DTC's frame id \n")
        dtc_dict = db.decode_message(msg.arbitration_id, msg.data) #hopefully decodes received message to a {signal name : values} dictionary
        #checkDTC()
        return 1

    #frame id for BMU_CellVoltage = 0x18800401
    elif (msg.arbitration_id == volts_msg.frame_id):
        print("Recevied msg.frame_id matches expected BMU_CellVoltage's frame id \n")
        volts_dict = db.decode_message(msg.arbitration_id, msg.data)
        #checkVolts()
        return 2

    #frame id for BMU_CellTemp = 0x18c00401
    elif (msg.arbitration_id == temp_msg.frame_id):
        print("Recevied msg.frame_id matches expected BMU_CellTemp's frame id \n")
        temp_dict = db.decode_message(msg.arbitration_id, msg.data)
        #checkTemps()
        return 3

    #frame id for PDU_ChannelStatus = 0x6
    elif (msg.arbitration_id == pdu_msg.frame_id):
        print("Recevied msg.frame_id matches expected PDU_ChannelStatus's frame id \n")
        pdu_dict = db.decode_message(msg.arbitration_id, msg.data)
        #checkPDUStatus()
        return 4

    else:
        print("Recevied message didn't match BMU_DTC or BMU_CellVoltage or BMU_CellTemp \n")
        return 0

#xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxo


# The following lines acn be used for module testing:
# i)    print_all_DTC()
# ii)   read_CAN_msg()


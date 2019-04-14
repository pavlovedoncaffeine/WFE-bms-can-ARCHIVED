# Waterloo Forumla Electric funcitons for CANBUS

import sys #to print without a newline? if comma doesn't work at the end of a print statement
import csv
import cantools
import pprint
import can


# db is an object of class cantools.database.can.Database()
# This contains the structure of all messages and their corresponding signals, signal names and relevant data as well
db = cantools.database.load_file('2018CAR.dbc')
# db complains about the masked frame id of "ChargeCart_ButtonEvents" and "TempCoolantRight"
# 

can_bus = can.interface.Bus(bustype='vector', appname = 'CANalyzer', channel = 0, bitrate=250000)
#can_bus = can.interface.Bus('vcan0', bustype='socketcan') 

#printobj = pprint.PrettyPrinter(indent=6)
DTCfile = open("DTC.csv", newline='\n')
readDTC = csv.reader(DTCfile)


#prints all DTC.csv cells to ensure all data is available 
def print_all_DTC():
    for row in readDTC:
        for cell in row:
            sys.stdout.write(cell + "\t\t"),
        print()
    #printobj.pprint(readDTC) Didn't work when trying to print a whole csv file

def read_BMU_DTC():
    msg = can_bus.recv()
    if (msg.arbitration_id == 0xff01):
        print("frame_id matches expected")
        dtc_msg = get_message_by_name("BMU_DTC")
    else:
        print("Didn't receive message or didn't match BMU_DTC frame_id")

# the following statements were used during testing
print_all_DTC()

#from cantools import *
import cantools

import can
from pprint import pprint

db = cantools.database.load_file('2018CAR.dbc')
can_bus = can.interface.Bus('testing', bustype='virtual')
#db is an object of class cantools.database.can.Database()
cellV_mux = db.get_message_by_name("BMU_CellVoltage")


#msg = can_bus.recv()
#decode to the relecant frame_id
#cellV_mux = db.decode_message(cellV_mux.frame_id, msg.data)


cellT_mux = db.get_message_by_name("BMU_CellTemp")
#print("Message is an extended frame: ", str(cellV_mux.is_extended_frame))
#print("Message is muxxed: ", str(cellV_mux.is_multiplexed()))

cellV_dict = cellV_mux.signal_tree[0].get('VoltageCellMuxSelect') # dictionary with mux signal key-value pairs
pprint(cellV_dict.values())
# printing and breaking down the mux signal into usable lists of three eachpprint(cellV_mux.)
#pprint(cellV_dict)

#------------------------------------------------------------------------------------
#print("\n Num of msgs: " + str(len(db.messages)) + "\n")

#print("Messages: ")
#cellV_msg = 
#cellV_msg = db.get_message_by_name("BMU_CellVoltage")

#for sig in cellV_msg.signals:
#	print(sig)

# print("Message is an extended frame: ", str(cellV_msg.is_extended_frame))
# print("Message is muxxed: ", str(cellV_msg.is_multiplexed))
# print("Signal tree:")
# print(cellV_msg.signal_tree)

# print("signal choices string: ?")
# print(cellV_msg.signal_choices_string())


# for msg in db.messages:
#     print(msg)
#     print("Signals: ")
#     for sig in msg.signals:
#         print(sig)
#     print("\n")
    
# print("Nodes: ")
# for node in db.nodes:
#     print(node)


#print()



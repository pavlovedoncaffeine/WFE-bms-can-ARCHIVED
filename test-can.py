import cantools
from pprint import pprint

db = cantools.database.load_file('2018CAR.dbc')
#db is an object of class cantools.database.can.Database()

print("\n Num of msgs: " + str(len(db.messages)) + "\n")

print("Messages: ")
for msg in db.messages:
    print(msg)
    print("Signals: ")
    for sig in msg.signals:
        print(sig)
    print("\n")
    
print("Nodes: ")
for node in db.nodes:
    print(node)


#print()



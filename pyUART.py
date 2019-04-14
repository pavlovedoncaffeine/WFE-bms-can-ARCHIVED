# Waterloo Forumla Electric 

import sys
import os
import serial

bmu_serial = serial.Serial('/dev/ttyUSB0') # EDIT | ASK ALEX WHAT PORT TO USE

bmu_serial.write(b'reset') #sending byes to reset the BMU over UART
# EDIT THE DATA BEING SENT OVER UART TO RESET THE BMU CORRECTLY

bmu_serial.close()

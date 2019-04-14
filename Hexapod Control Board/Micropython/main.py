import webrepl
from machine import UART
import time
print(webrepl.start())


uart=UART(0,9600)
##
#uart.init(9600, bits=8, parity=None, stop=1)
##
while True:
    print("No UART")
    input1=input("Read Serial Line? Y/N")
    time.sleep(0.5)
####    if input1=='Y':
####        print(uart.read())
##    else:
##        continue
##    
##
##

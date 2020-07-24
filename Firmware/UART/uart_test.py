from machine import UART

uart = UART(1, 19200)                         # init with given baudrate
uart.init(19200, bits=8, parity=None, stop=1) # init with given parameters

if uart.any():
    buff = uart.readall()
    print (buff)
    
uart.write('C')
print ("write cmplt")
time.sleep(2)
if uart.any():
    buff1 = uart.readall()# read up to 5 bytes
else:
    buff1 ="nothing"
#uart.readinto(buf)
print ("output")
print (buff1)


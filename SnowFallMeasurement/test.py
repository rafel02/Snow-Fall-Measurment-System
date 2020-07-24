import pycom
import time
import machine

pycom.heartbeat(False)

i =2
while i:
    pycom.rgbled(0x00007f) # blue
    time.sleep(1)
    pycom.rgbled(0x007f00) # green
    time.sleep(1)
    i-=1

pycom.heartbeat(True)

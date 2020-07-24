import pycom
import time
import machine

pycom.heartbeat(False)
while True:
    pycom.rgbled(0x00007f) # blue
    time.sleep(1)
    pycom.rgbled(0x007f00) # green
    time.sleep(1)

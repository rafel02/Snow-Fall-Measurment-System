import machine
from network import WLAN
import pycom
import time
wlan = WLAN() # get current object, without changing the mode

pycom heartbeat(Fals)
print('led on')
pycom rgbled(0x7f0000)  # red

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=('192.168.178.107', '255.255.255.0', '192.168.178.1', '8.8.8.8'))

print('STATIC IP = 192.168.178.107')

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect('TTU', auth=(WLAN.WPA2, ''), timeout=5000)
    print('wifi connecting')
    while not wlan.isconnected():
        machine.idle() # save power while waiting
wlan = WLAN()

pycom.rgbled(0x00007f) # blue

time.sleep(1)
pycom.rgbled(0x007f00) # green
print(wlan.ifconfig())

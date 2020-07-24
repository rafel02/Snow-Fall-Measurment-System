from network import LoRa
import socket
import time
import binascii

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)#, frequency=868100000)

# create an OTAA authentication parameters
#app_eui = binascii.unhexlify('70 B3 D5 7E D0 00 96 EB'.replace(' ',''))
#app_key = binascii.unhexlify('98 71 B5 2B A5 CE 70 94 EA 2F B9 9A 4C D9 64 24'.replace(' ',''))
#app_eui = binascii.unhexlify('70 b3 d5 7e d0 00 96 eb'.replace(' ',''))
#app_key = binascii.unhexlify('98 71 b5 2b a5 cd 70 94 ea 2f b9 9a 4c d9 64 24'.replace(' ',''))
app_eui = binascii.unhexlify('00 00 00 00 00 00 00 00'.replace(' ',''))
app_key = binascii.unhexlify('00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'.replace(' ',''))
dev_eui = binascii.unhexlify ('70 b3 d5 49 96 67 ee a8'.replace(' ',''))
# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
#lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.0)
    print('Not yet joined...')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# send some data
s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print(data)

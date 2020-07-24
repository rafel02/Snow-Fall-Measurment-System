from network import LoRa
import socket
import binascii
import struct

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('26 01 1B 6C'.replace(' ','')))[0]
nwk_swkey = binascii.unhexlify('9E 47 98 83 D1 D7 EE 7A 93 E2 F6 85 AD 8E 13 2F'.replace(' ',''))
app_swkey = binascii.unhexlify('FE B8 6A 5E B8 8C 46 AD C4 04 E2 AC D0 08 5E C9'.replace(' ',''))

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blockinga
# (waits for the data to be sent and for the 2 receive windows to expire)
count =1;
while 1:
    s.setblocking(True)

    # send some data
    s.send(bytes([46 , 335]))
    time.sleep(2)
    s.send(bytes([43 , 215]))

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print('Packet count: ',count,' Received data:',data)
    #print(data)
    count+=1
    time.sleep(2)

from network import LoRa
import socket
import time
import binascii
import utime

def select_subband(lora, subband):
    if (type(subband) is int):
        if ((subband<1) or (subband>8)):
            raise ValueError("subband out of range (1-8)")
    else:
        raise TypeError("subband must be 1-8")

    for channel in range(0, 72):
       lora.remove_channel(channel)

    index = (subband-1)*8
    for channel in range(0, 7):
        lora.add_channel(channel, frequency=902300000+index*200000, dr_min=0, dr_max=3)
        index+=1

    index = (subband-1)*8
    for channel in range(8, 15):
        lora.add_channel(channel, frequency=902300000+index*200000, dr_min=0, dr_max=3)
        index+=1

    index = (subband-1)*8
    for channel in range(16, 23):
        lora.add_channel(channel, frequency=902300000+index*200000, dr_min=0, dr_max=3)
        index+=1

    index = (subband-1)*8
    for channel in range(24, 31):
        lora.add_channel(channel, frequency=902300000+index*200000, dr_min=0, dr_max=3)
        index+=1

    index = (subband-1)*8
    for channel in range(32, 39):
        lora.add_channel(channel, frequency=902300000+index*200000, dr_min=0, dr_max=3)
        index+=1

    index = (subband-1)*8
    for channel in range(40, 47):
        lora.add_channel(channel, frequency=902300000+index*200000, dr_min=0, dr_max=3)
        index+=1

    index = (subband-1)*8
    for channel in range(48, 55):
        lora.add_channel(channel, frequency=902300000+index*200000, dr_min=0, dr_max=3)
        index+=1

    index = (subband-1)*8
    for channel in range(56, 63):
        lora.add_channel(channel, frequency=902300000+index*200000, dr_min=0, dr_max=3)
        index+=1

    index = (subband-1)*8
    for channel in range(64, 71):
        lora.add_channel(channel, frequency=902300000+index*200000, dr_min=0, dr_max=3)
        index+=1

lora = LoRa(mode=LoRa.LORAWAN)#, adr=False, public=True, tx_retries=0)

sb = 2 #Change to desired conduit frequency sub-band

select_subband(lora,sb)

app_eui = binascii.unhexlify('00 00 00 00 00 00 00 00'.replace(' ',''))
app_key = binascii.unhexlify('00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'.replace(' ',''))

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

while not lora.has_joined():
    time.sleep(5)
    print('Not yet joined on frequency sub-band '+str(sb)+'...')

if(lora.has_joined()):print("Successful join on frequency sub-band "+str(sb)+"!")

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

pressure = 100

while lora.has_joined():
    payload = '{"pressure":'+str(pressure)+',"tst":'+str(utime.time())+'}'
    print(payload)
    s.send(payload)
    time.sleep(6)

    pressure +=1

    if pressure > 100:
        pressure = 1

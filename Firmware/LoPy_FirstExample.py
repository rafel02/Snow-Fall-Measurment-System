from network import LoRa
import socket
import machine
import time

# initialize LoRa in LORA mode
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

while True:
    # send some data
    s.setblocking(True)
    s.send('Hello')
    print("Tx Done")
    # get any data received...
    s.setblocking(False)
    data = s.recv(64)
    print("Rx Done")
    print(data)

    # wait a random amount of time
    time.sleep(machine.rng() & 0x0F)

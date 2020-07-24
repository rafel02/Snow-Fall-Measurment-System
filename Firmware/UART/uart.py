from machine import UART
import time

data = []
uart_baud = 19200
uart = UART(1, uart_baud)
open_cmd = 'O'
close_cmd = 'C'
dist_cmd = 'D'
tem_pwr_cmd = 'S'

def uart_init():
	print ("Intilizing UART")
	uart.init(uart_baud, bits=8, parity=None, stop=1) # init with given parameters
	time.sleep(2)

def clear_data():
	list_index = len(data)-1
	while (list_index >= 0 ):
		data.pop(list_index)
		list_index = len(data)-1
	#print ('Clear data : {}\n'.format(data))

def set_distance(rsp_str):
	dis_rsp ='D:'
	#rsp_str = 'D: 0.330m, 1480'	#for testing

	base = int(rsp_str.find(dis_rsp))
	print (base)
	try:
		if( rsp_str[base+8] == 'm'):
			dist = float(rsp_str[base+3:base+8])
		else:
			dist = float(rsp_str[base+3:base+9])
		print ('Distance : {} m'.format(dist))
		dist = int( dist *1000)
		data.insert( 0,(dist >> 8)  )
		data.insert( 1,(dist & 0xFF))
		return 0
	except Exception as ValueError:
		print ("Invalid response")
		return -1

#def set_temppwr(rsp_str)

def readdata(exp_rsp):
	if uart.any():
		uart_buff = str(uart.readall())
		print ('Response packet : {}'.format(uart_buff))
		if uart_buff.find(exp_rsp) >= 0:
			#print ("Response match")
			return uart_buff
			#return 'D: 11.223dd'
		else:
			print ("Response doesn't match")
			return -1
	else:
		print ("No response")
		return -1

def cmd_rsp(cmd, exp_rsp):
	#print (cmd)
	uart.write(cmd)
	time.sleep(3)
	rsp = readdata(exp_rsp)
	time.sleep(2)
	if -1 != rsp:
		return rsp
	else:
		return -1;

while 1:
	count = 0
	uart_init()
	while (-1 == cmd_rsp(open_cmd ,'O,OK') and count < 3):
		print ("Fail to open UART, Retrying")
		time.sleep(2)
		count +=1

	if (count < 3):
		print ('UART opened')

	while (count <3):
		rsp = cmd_rsp(dist_cmd,'D:')
		if (-1 != rsp):
			if( -1 != set_distance(rsp) ):
				rsp = cmd_rsp(tem_pwr_cmd ,'S:')
				if (-1 != rsp):
					#set_temppwr(rsp)
					print('Data Pack : {}'.format(data))
					count =0
				else:
					count +=1
		clear_data()					#clearing buffer for next cycle
		time.sleep(5)

	count=0
	while (-1 == cmd_rsp(close_cmd ,'C,OK') and count < 3):
		time.sleep(2)
		print ("Fail to close UART, Restrying")
		count +=1

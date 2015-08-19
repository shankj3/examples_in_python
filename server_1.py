import socket
import sys

HOST = ''
PORT = 8889

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket Created')

#binding to local host and PORT
try:
	s.bind((HOST,PORT))
except socket.erros as msg:
	print("Bind failed. Error Code: %s Message %s" %(msg[0],msg[1]))
	sys.exit()
print( 'Socket bind complete')

#listen on socket
s.listen(10)
print( 'Scoket now listening')

#now keep talking with client
while 1:
	#wait to accept connection-blocking call
	conn, addr = s.accept()
	print('Connected with %s : %s' %(addr[0], addr[1]))
s.close()
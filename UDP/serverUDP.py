import socket
import threading
import sys

# Funcao responsavel por esperar a mensagem de parada do client
def waitMsg():
	global conn, finished

	conn.recv(1024)
	finished = True

# Funcao responsavel por testar a taxa de download
def download():
	global sockData, finished, conn

	thr = threading.Thread(target=waitMsg)
	thr.start()
	msg = bytes(100)
	
	packCounter = 0

	while True:
		sockData.sendto(msg, ADDR)

		if finished: break
		packCounter += 1
	
	conn.send(f'{packCounter}'.encode('utf-8'))

# Funcao responsavel por testar a taxa de upload
def upload():
	global sockData, finished, conn

	thr = threading.Thread(target=waitMsg)
	thr.start()

	buff = bytes(0)

	packCounter = 0

	while True:
		try:
			buff += sockData.recv(100)
			packCounter += 1
		except socket.timeout:
			pass

		if finished: break
	
	conn.send(f'{len(buff)}'.encode('utf-8'))
	conn.send(f'{packCounter}'.encode('utf-8'))

try:
	IP = sys.argv[1]
	PORT = int(sys.argv[2])
except IndexError:
	print('Deve ser inserido IP e PORTA via argumento do programa')
	exit()

ADDR = (IP, PORT)

# Abrindo e configurando o socket de dados para enviar pacotes pro client
sockData = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockData.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Abrindo e configurando o socket de mensagens responsável por enivar e receber infos do client
sockMsg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockMsg.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockMsg.bind(('', PORT))
sockMsg.listen(1)

# Espera o client se conectar com o server
conn, addr = sockMsg.accept()
print(f'Conectado a {addr[0]}')

finished = False
download()

# Reconfigurando socket de dados para receber pacotes do client
sockData = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockData.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockData.bind(ADDR)
sockData.settimeout(0.1)

finished = False
upload()

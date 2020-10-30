import socket
import threading
import time
import sys

INTERVAL = 20

# Funcao responsavel por testar a taxa de download
def download():
	global sockData, sockMsg

	start = time.time()
	totalTime = 0
	buff = bytes(0)

	packCounter = 0

	# Recebendo pacotes
	while True:
		[pack, _] = sockData.recvfrom(100)
		buff += pack
		packCounter += 1

		totalTime = time.time()-start
		if (totalTime) >= INTERVAL:
			break

	# Envia uma mensagem pro server parar de enviar pacotes
	sockMsg.send(b'OK')
	pcs = int(sockMsg.recv(100).decode('utf-8'))

	kbs = len(buff) / totalTime / 1024 * 8
	packss = packCounter / totalTime
	tpp = abs(pcs - packCounter) / totalTime

	print("DOWNLOAD:")
	print( 'Velocidadedos bytes:      %.2f Kb/s' % kbs)
	print( 'Velocidade pacotes:       %.2f pacotes/s' % packss)
	print(f'Qtd. bytes:               {len(buff)} bytes')
	print( 'Tempo:                    %.2f segundos' % totalTime)
	print( 'Taxa de perda de pacotes: %.2f pacotes/s' % tpp)

# Funcao responsavel por testar a taxa de upload
def upload():
	global sockData, sockMsg

	msg = bytes(100)

	start = time.time()
	totalTime = 0

	packCounter = 0
	
	# Enviando pacotes
	while True:
		sockData.sendto(msg, ADDR)
		packCounter += 1
	
		totalTime = time.time()-start
		if (totalTime) >= INTERVAL:
			break
	
	sockMsg.send(b'OK')
	bufSize = int(sockMsg.recv(100).decode('utf-8'), 10)
	pcs = int(sockMsg.recv(100).decode('utf-8'), 10)

	kbs = bufSize / totalTime / 1024 * 8
	packss = packCounter / totalTime
	tpp = abs(pcs - packCounter) / totalTime

	print("UPLOAD:")
	print( 'Velocidadedos bytes:      %.2f Kb/s' % kbs)
	print( 'Velocidade pacotes:       %.2f pacotes/s' % packss)
	print(f'Qtd. bytes:               {bufSize} bytes')
	print( 'Tempo:                    %.2f segundos' % totalTime)
	print( 'Taxa de perca de pacotes: %.2f pacotes/s' % tpp)

# pega os argumentos passados na chamada do programa
try:
	IP = '177.40.76.120'
	PORT = 1234
except IndexError:
	print('Deve ser inserido IP e PORTA via argumento do programa')
	exit()

ADDR = (IP, PORT)

# Abrindo e configurando o socket de dados para receber pacotes do server
sockData = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockData.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockData.bind(('0.0.0.0', PORT))

# Abrindo e configurando o socket de mensagens responsável por enivar e receber infos do server
sockMsg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockMsg.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockMsg.connect(ADDR)

download()

# Reconfigurando socket de dados para enviar pacotes pro server
sockData = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockData.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print('\n')
upload()

input("Pressione Enter para sair.")
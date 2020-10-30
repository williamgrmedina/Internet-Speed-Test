import socket
import imports as imp
import time
import random
import string
import sys

s = socket.socket()

host = input('IP: ')
port = int(input('Port: '))

data = ('a' * imp.SIZE_PACKS).encode(imp.CODIFIC)

s.connect((host, port))
print('iniciando teste de download...')

receivedList = []

#download test
packets = 0
end = 0
time_passed = 0
cur_interval = 0
begin = time.time()

while time_passed < 15:
    cur_interval_begin = time.time()
    while cur_interval < imp.UPDATE_INTERVAL and time_passed < 15:
        received = s.recv(imp.SIZE_PACKS)
        packets += 1
        time_passed = time.time() - begin
        cur_interval = time.time() - cur_interval_begin
        cur_speed = (packets * imp.SIZE_PACKS * 8) / (1000000 * time_passed)
    print(f'{cur_speed}')
    cur_interval = 0

print(f'pacotes recebidos client: {packets}')
print(f'iniciando teste de upload...')

#upload test
packets = 0
end = 0
time_passed = 0
begin = time.time()

while time_passed < 15:
    while cur_interval < imp.UPDATE_INTERVAL and time_passed < 15:
        s.send(data)
        packets += 1
        time_passed = time.time() - begin
    cur_interval = 0

#print(f'Tamanho dos pacotes enviados: {imp.SIZE_PACKS}')
print(f'pacotes enviados: {packets}')

while True: 
    var = str.lower(input("Digite a senha: "))
    if var == "eu te amo" or var == "te amo" or var == "william lindo":
        s.send(var.encode(imp.CODIFIC))
        break
    
s.close()
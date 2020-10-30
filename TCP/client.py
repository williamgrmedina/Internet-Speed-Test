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

################################  download test  ################################
packets = 0
end = 0
time_passed = 0
begin = time.time()

while time_passed < 15:
    cur_interval = 0
    interval_start = time.time()
    
    # receives data sent from server in packets and displays current speed at every interval end,
    # or when given test time limit is reached
    while cur_interval < imp.UPDATE_INTERVAL and time_passed < 15:
        packet = s.recv(imp.SIZE_PACKS).decode(imp.CODIFIC)
        split_packet = packet.split(" ", 1)
        packet_num = split_packet[0]
        packet_data = split_packet[1]
        print(f'packet num: {packet_num}')
        print(f'packet data: {packet_data}')
        packets += 1
        time_passed = time.time() - begin

        cur_interval = time.time() - interval_start
        if time_passed > 0:
            cur_speed = (packets * imp.SIZE_PACKS * 8) / (1000000 * time_passed)
    
    print(f'{cur_speed}')

print(f'pacotes recebidos client: {packets}')
print(f'iniciando teste de upload...')
#################################################################################

################################  upload test    ################################
packets = 0
end = 0
time_passed = 0
begin = time.time()

while time_passed < 15:
    cur_interval = 0
    interval_start = time.time()

    # uploads data in packets and displays current speed at every interval end,
    # or when given test time limit is reached
    while cur_interval < imp.UPDATE_INTERVAL and time_passed < 15:
        s.send(data)
        packets += 1
        time_passed = time.time() - begin

        cur_interval = time.time() - interval_start
        if time_passed > 0:
            cur_speed = (packets * imp.SIZE_PACKS * 8) / (1000000 * time_passed)
    
    print(f'{cur_speed}')
#################################################################################



#print(f'Tamanho dos pacotes enviados: {imp.SIZE_PACKS}')
print(f'pacotes enviados: {packets}')

while True: 
    var = str.lower(input("Digite a senha: "))
    if var == "eu te amo" or var == "te amo" or var == "william lindo" or var == "pai ta on":
        s.send(var.encode(imp.CODIFIC))
        break
    
s.close()
import socket
import imports as imp
import time
import os, sys

port = int(input('Port: '))
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = ''
s.bind((host, port))
s.listen(5)

while True:
    print('Server esperando conexao....')

    conn, addr = s.accept()
    print(f'{addr} Conectou\n')

    data = ('a' * imp.SIZE_PACKS)
    packets = 0
    begin = time.time()
    time_passed = 0
    byte_count = 0

    #download test
    while time_passed < 15:
        byte_count = byte_count + conn.send( (data).encode(imp.CODIFIC))
        packets += 1
        time_passed = time.time() - begin

    print(f'bytes: {byte_count}')
    print(f'pacotes enviados do serv: {packets}')
    conn.send(str(packets).encode(imp.CODIFIC))

    # upload test
    packets = 0
    begin = time.time()
    time_passed = 0

    while time_passed < 15:
        data = conn.recv(imp.SIZE_PACKS)
        if not data:
            print("no data")
            break
        packets += 1
        time_passed = time.time() - begin

    print(f'pacotes recebidos: {packets}')

    #print(f"Tamanho do arquivo (Bytes): {size}")
    #print(f"Tamanho dos pacotes (Bytes): {imp.SIZE_PACKS}")
    #print(f"Numero de pacotes recebidos: {packets}")
    #print(f"Velocidade (bits/s): {size*8/(end-begin)}")


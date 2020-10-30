import socket
import imports as imp
import time
import errno
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
    conn.setblocking(False)

    print(f'{addr} Conectou\n')

    data = ('a' * (imp.SIZE_PACKS))
    packets = 0
    begin = time.time()
    time_passed = 0
  
                   
    def download_test(begin, time_passed, packets):
        try:
            while time_passed < 15: 
                prefix = str(packets) + ' '
                data = prefix + ('a' * (imp.SIZE_PACKS - len(prefix)) ) 
                print(f'{len(data)}  {time_passed}')
                conn.send(data.encode(imp.CODIFIC))
                packets += 1
                time_passed = time.time() - begin
        except IOError:
            # continua mandando pacotes mesmo se houver erro 
            # ate que atinja segundos determinados
            time.sleep(0.3)
            time_passed += 0.3
            download_test(begin, time_passed, packets)
                
    download_test(begin, time_passed, packets)
    print(f'pacotes enviados do serv: {packets}')

    # upload test

    packets = 0
    begin = time.time()
    time_passed = 0
    conn.setblocking(True)

    while time_passed < 15:
        data = conn.recv(imp.SIZE_PACKS)
        if not len(data):
            print("no data")
            break
        packets += 1
        time_passed = time.time() - begin

    print(f'pacotes recebidos: {packets}')

    #print(f"Tamanho do arquivo (Bytes): {size}")
    #print(f"Tamanho dos pacotes (Bytes): {imp.SIZE_PACKS}")
    #print(f"Numero de pacotes recebidos: {packets}")
    #print(f"Velocidade (bits/s): {size*8/(end-begin)}")


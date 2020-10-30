import socket
import imports as imp
import time
import errno
import os, sys

# manda strings de pacotes no formato 
# <numero do pacote> <" "> <conteudo do pacote>

# numero do pacote: int de 1 a MAX_INT (atualizado a cada envio, sequencialmente)
# " ": espaco utilizado como separador para cliente saber quando conteudo de fato comeca 
# conteudo do pacote: conteudo sempre fixo de char 'a' * tamanho definido
# com cuidados especiais tomados (representar dezena exige mais bits do que unidade)
def download_test(begin, time_passed, packets):
        try:
            while time_passed < imp.TEST_TIME: 
                prefix = str(packets) + ' '
                data = prefix + ('a' * (imp.SIZE_PACKS - len(prefix)) ) 
                print(f'{len(data)}  {time_passed}')
                conn.send(data.encode(imp.CODIFIC))
                packets += 1
                time_passed = time.time() - begin
            print(f'pacotes enviados do serv: {packets}')
        except IOError:
            # continua mandando pacotes mesmo se houver erro 
            # ate que atinja tempo determinado
            time.sleep(0.3)
            time_passed += 0.3
            download_test(begin, time_passed, packets)



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
                
    download_test(begin, time_passed, packets)

    # upload test
    packets = 0
    begin = time.time()
    time_passed = 0
    conn.setblocking(True)

    try: 
        while True:
            data = conn.recv(imp.SIZE_PACKS)
            if not len(data):
                print("no data has been sent to server. Closing connection.")
                conn.close()
                break
            packets += 1
            time_passed = time.time() - begin
    except IOError:
        print("connection has been closed by client.")
        print(f'pacotes recebidos: {packets}')

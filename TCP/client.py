import socket
import imports as imp
import time
import random
import string
import sys

#procura e salva indice dos pacotes que não foram recebidos
def getLostPackets(packet_num_list):
    lost_packets = []
    for i in range(len(packet_num_list) - 1):
        expected_value = packet_num_list[i] + 1
        found_value = packet_num_list[i+1]
        
        if found_value > expected_value: 
            # one or more packets were not received. Recover their indexes
            while found_value > expected_value:
                lost_packets.append(expected_value)
                expected_value += 1
    return lost_packets




s = socket.socket()

host = input('IP: ')
port = int(input('Port: '))

data = ('a' * imp.SIZE_PACKS).encode(imp.CODIFIC)

print('iniciando teste de download...')
time.sleep(2)
s.connect((host, port))
################################  download test  ################################
packets = 0
end = 0
time_passed = 0
begin = time.time()
packet_recvd_list = []

while time_passed < imp.TEST_TIME:
    cur_interval = 0
    interval_start = time.time()
    
    # receives data sent from server in packets and displays current speed at every interval end
    # until given test time limit is reached
    while cur_interval < imp.UPDATE_INTERVAL and time_passed < imp.TEST_TIME:
        packet = s.recv(imp.SIZE_PACKS).decode(imp.CODIFIC)
        
        # saves index of packet received in packet_recvd_list
        # this list will be used to check for packet loss
        # if all packets were received, then the list when sorted should be linear
        split_packet = packet.split(" ", 1)
        if split_packet:
            packet_num = int(split_packet[0])
            packet_recvd_list.append(packet_num)
            packets += 1
        
        time_passed = time.time() - begin

        cur_interval = time.time() - interval_start
        if time_passed > 0:
            cur_speed = (packets * imp.SIZE_PACKS * 8) / (1000000 * time_passed)
    
    print(f'{cur_speed:.2f} Mb/s')

# ordena e calcula indices dos pacotes perdidos
packet_recvd_list.sort()
lost_packets = getLostPackets(packet_recvd_list)

print(f'pacotes recebidos: {packets}')
print(f'pacotes perdidos: {len(lost_packets)}')
print(f'taxa de perda de pacotes: {(len(lost_packets) / packets):.2f}%')

time.sleep(3)
print(f'iniciando teste de upload...')
time.sleep(2)
#################################################################################

################################  upload test    ################################
packets = 0
end = 0
time_passed = 0
begin = time.time()

while time_passed < imp.TEST_TIME:
    cur_interval = 0
    interval_start = time.time()

    # uploads data in packets and displays current speed at every interval end,
    # or when given test time limit is reached
    while cur_interval < imp.UPDATE_INTERVAL and time_passed < imp.TEST_TIME:
        s.send(data)
        packets += 1
        time_passed = time.time() - begin

        cur_interval = time.time() - interval_start
        if time_passed > 0:
            cur_speed = (packets * imp.SIZE_PACKS * 8) / (1000000 * time_passed)
    
    print(f'{cur_speed:.2f} Mb/s')
#################################################################################



print(f'pacotes enviados: {packets}')
print(f'Tamanho dos pacotes: {imp.SIZE_PACKS}')
print(f'velocidade media de envio: {(packets * imp.SIZE_PACKS * 8) / (1000000 * imp.TEST_TIME):.2f} Mb/s')

input("\nProcesso finalizado. Pressione Enter para fechar a janela.")
    
s.close()
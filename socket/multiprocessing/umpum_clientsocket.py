import socket
import multiprocessing
import random
import time


## Client Socket

host = '127.0.0.1'
port = 6007
addr = (host, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Client Socket Created')
client_socket.connect(addr)
print('Client Socket Connected')


## Process Messaging

'''def gera_num():
    return random.randint(1, 100)'''

def send_num(num):
    time.sleep(0.1)
    message = str(num)

    print('{} enviado para {}'.format(message, *addr))
    client_socket.sendto(message.encode(), addr)

    while(True):
        message_received = client_socket.recv(1024)
        if(message_received):
            print('{} recebido de {}'.format(message_received, *addr))
            break


proc = multiprocessing.Process(target = send_num, args = (random.randint(1, 100),))
proc.start()
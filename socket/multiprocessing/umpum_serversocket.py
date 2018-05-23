import socket
import multiprocessing
import random
import time


## Server Socket

host = '127.0.0.1'
port = 6007
addr = (host, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server Socket Created')
server_socket.bind(addr)
server_socket.listen(1)
print('Client Socket Waiting')

## Process Messaging

def receive_num():
    while(True):
        connection, client_addr = server_socket.accept()
        print('{} is connected'.format(client_addr))

        while(True):
            message_received = connection.recv(1024)
            if(message_received):
                print('{} recebido de {}'.format(message_received, client_addr))
                break

            
        message = str(message_received)
        connection.sendto(message.encode(), client_addr)
        print('{} enviado para {}'.format(message, client_addr))
        break

    connection.close()



proc = multiprocessing.Process(target = receive_num)
proc.start()
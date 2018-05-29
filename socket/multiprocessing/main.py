import socket
import multiprocessing as mp
import os
import random
import time
import queue


## Process Information

QTD_SERVER_PROCS = 1
QTD_SERVER_PROCS_COUNTER = 0
QTD_CLIENT_PROCS = 1
QTD_CLIENT_PROCS_COUNTER = 0
q = queue.Queue()

## Sockets Information

host = '127.0.0.1'
port = 2426
addr = (host, port)


## Sockets
'''
server_socket = mp.Queue()
for i in range(QTD_SERVER_PROCS):
    server_socket.put(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
client_socket = mp.Queue()
for i in range(QTD_CLIENT_PROCS):
    client_socket.put(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
'''

## Functions

def rnum():
    return random.randint(1, 100)

def enfileirando(q):
    q.put(rnum())


## Starting Sockets

def server_start():
    global QTD_CLIENT_PROCS_COUNTER
    global QTD_SERVER_PROCS_COUNTER
    #server = server_socket.get()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server-{} started".format(os.getpid()))
    server.bind(addr)
    server.listen(QTD_CLIENT_PROCS)
    while(True):
        connection, client_addr = server.accept()
        while(QTD_CLIENT_PROCS_COUNTER < QTD_CLIENT_PROCS):
            message_received = connection.recv(64)
            #print("{} received".format(message_received))
            if not message_received:
                break
            print("Server-{} received {}".format(os.getpid(), message_received))
            QTD_CLIENT_PROCS_COUNTER += 1
        print('teste1')
        QTD_SERVER_PROCS_COUNTER += 1
        break
    print('teste2')
    connection.close()

def client_start(num):
    time.sleep(0.2)
    #client = client_socket.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client-{} started".format(os.getpid()))
    client.connect(addr)

    message = str(num)
    client.sendto(message.encode(), addr)


## main

#if __name__ == 'main':
server_proc = mp.Process(target=server_start)
server_proc.daemon = True
client_proc = mp.Process(target=client_start, args=(rnum(), ))
client_proc.daemon = True
server_proc.start()
#server_proc.join()
client_proc.start()
server_proc.join()
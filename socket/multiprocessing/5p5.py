import socket
import multiprocessing as mp
import os
import random
import time


## Process Information

QTD_SERVER_PROCS = 5
QTD_SERVER_PROCS_COUNTER = 0
QTD_CLIENT_PROCS = 5
QTD_CLIENT_PROCS_COUNTER = 0


## Sockets Information

host = '127.0.0.1'
port = 2427
addr = (host, port)


## Sockets

server_procs = []
client_procs = []


## Functions

def rnum():
    return random.randint(1, 100)


## Starting Sockets

def server_start():
    time.sleep(1)
    global QTD_CLIENT_PROCS_COUNTER
    global QTD_SERVER_PROCS_COUNTER
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Server-{} started".format(os.getpid()))
    server.bind(addr)
    server.listen(QTD_CLIENT_PROCS)
    while(True):
        connection, client_addr = server.accept()
        while(QTD_CLIENT_PROCS_COUNTER < QTD_CLIENT_PROCS):
            message_received = connection.recv(64)
            if not message_received:
                break
            print("Server-{} received {}".format(os.getpid(), message_received))
            QTD_CLIENT_PROCS_COUNTER += 1
        print('teste1')
        QTD_SERVER_PROCS_COUNTER += 1
        if(QTD_CLIENT_PROCS_COUNTER == QTD_CLIENT_PROCS):
            QTD_CLIENT_PROCS_COUNTER = 0
            break
    print('teste2')
    connection.close()

def client_start(num):
    time.sleep(2)
    #client = client_socket.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client-{} started".format(os.getpid()))
    client.connect(addr)

    message = str(num)
    client.sendto(message.encode(), addr)


#if __name__ == 'main':


for sp in range(QTD_SERVER_PROCS):
    server_procs.append(mp.Process(target=server_start))
    server_procs[sp].daemon = True

for cp in range(QTD_CLIENT_PROCS*QTD_SERVER_PROCS):
    client_procs.append(mp.Process(target=client_start, args=(rnum(), )))
    client_procs[cp].daemon = True

for i in range(QTD_SERVER_PROCS):
    server_procs[i].start()
    for j in range(QTD_CLIENT_PROCS):
        client_procs[j].start()
        client_procs[j].join()
    del client_procs[0:5]
    server_procs[i].join()

import socket
import multiprocessing as mp
import os
import random
import time


## Informations

QTD_SERVER_PROCS = 5
QTD_CLIENT_PROCS = 5
total_time = 0

host = '127.0.0.1'
port = (2424, 2425, 2426, 2427, 2428)
addr = [(host, port[0]), (host, port[1]), (host, port[2]), (host, port[3]), (host, port[4])]


## Sockets

server_procs = []
client_procs = []


## defs


def rnum():
    return random.randint(1, 100)


def server_start(prts):
    #time.sleep(0.2)
    messages_counter = 0

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr[prts])
    server.listen(QTD_CLIENT_PROCS)
    print("Server-{} started in {} and listening...".format(os.getpid(), addr[prts]))

    while(messages_counter < QTD_CLIENT_PROCS):
        (connection, client_addr) = server.accept()
        message_received = connection.recv(64)
        if(not message_received):
            #time.sleep(0.5)
            break
        print("Server-{} received {} from {}".format(os.getpid(), message_received, client_addr))
        messages_counter += 1
        print("msg_count_server->{}".format(messages_counter))
        connection.close()
        #print("")
        #time.sleep(0.1)


def client_start(num):
    #time.sleep(0.4)
    messages_counter = 0
    print("")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client-{} started".format(os.getpid()))
    message = str(num)

    while(messages_counter < QTD_SERVER_PROCS):
        client.connect(addr[messages_counter])
        client.send(message.encode())
        print("Client-{} send {} for {}".format(os.getpid(), message, addr[messages_counter]))
        messages_counter += 1
        print("msg_count_client->{}".format(messages_counter))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #time.sleep(0.2)


def cincopcinco():
    for sp in range(QTD_SERVER_PROCS):
        server_procs.append(mp.Process(target=server_start, args=(sp, )))
        server_procs[sp].daemon = True

    for cp in range(QTD_CLIENT_PROCS):
        client_procs.append(mp.Process(target=client_start, args=(rnum(), )))
        client_procs[cp].daemon = True

    for i in range(QTD_SERVER_PROCS):
        server_procs[i].start()

    for j in range(QTD_CLIENT_PROCS):
        client_procs[j].start()
        client_procs[j].join()
        #server_procs[i].join()

if __name__ == "__main__":
    total_time = time.time()
    cincopcinco()
    print("\n\nTime spent: {}".format(time.time() - total_time))

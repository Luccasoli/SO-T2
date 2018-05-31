import socket
import multiprocessing as mp
import os
import random
import time


## Process Information

QTD_SERVER_PROCS = 5
QTD_SERVER_PROCS_COUNTER = 0
QTD_CLIENT_PROCS = 1
QTD_CLIENT_PROCS_COUNTER = 0


## Sockets Information

host = '127.0.0.1'
port = (2424, 2425, 2426, 2427, 2428)
addr = [(host, port[0]), (host, port[1]), (host, port[2]), (host, port[3]), (host, port[4])]


## Sockets

server_sockets = []
server_procs = []
client_sockets = []
client_procs = []

for i in range(QTD_SERVER_PROCS):
    server_sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

for i in range(QTD_CLIENT_PROCS):
    client_sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))


## Functions

def rnum():
    return random.randint(1, 100)


## Starting Sockets

def server_start(pos):
    time.sleep(0.2)
    messages_counter = 0

    try:
        server = server_sockets[pos]
        server.bind(addr[pos])
        server.listen(QTD_CLIENT_PROCS)

        try:
            while(True):
                if(messages_counter == QTD_CLIENT_PROCS):
                    break
                (connection, client_addr) = server.accept()
                    
                while(messages_counter < QTD_CLIENT_PROCS):
                    message_received = connection.recv(1024)
                    if(not message_received):
                        break
                    print("Server-{} received {}".format(os.getpid(), message_received))
                    messages_counter += 1
                    print("smessages_count->{}".format(messages_counter))
        except Exception:
            print("err 2")

    except Exception:
        print("err 1")
    finally:
        connection.close()
        print("ok 1")
    

def client_start(num, pos):
    time.sleep(1)
    messages_counter = 0

    try:
        client = client_sockets[pos]
        message = str(num)

        try:
            while(True):
                client.connect(addr[messages_counter])
                if(messages_counter == QTD_SERVER_PROCS):
                    break
                    while(messages_counter < QTD_SERVER_PROCS):
                        client.sendto(message.encode(), addr[messages_counter])
                        messages_counter += 1
                        print("cmessages_count->{}".format(messages_counter))

        except Exception:
            print("err 4")

    except Exception:
        print("err 3")
    finally:
        print("ok 2")

for sp in range(QTD_SERVER_PROCS):
    server_procs.append(mp.Process(target=server_start, args=(sp, )))
    server_procs[sp].daemon = True

for cp in range(QTD_CLIENT_PROCS):
    client_procs.append(mp.Process(target=client_start, args=(rnum(), cp)))
    client_procs[cp].daemon = True

for i in range(QTD_SERVER_PROCS):
    server_procs[i].start()

for j in range(QTD_CLIENT_PROCS):
    client_procs[j].start()
    client_procs[j].join()
    #server_procs[i].join()
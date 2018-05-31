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
port = (2424, 2425, 2426, 2427, 2428)
addr = [(host, port[0]), (host, port[1]), (host, port[2]), (host, port[3]), (host, port[4])]


## Sockets

server_procs = []
client_procs = []


## Functions

def rnum():
    return random.randint(1, 100)


## Starting Sockets

def server_start(prts):
    time.sleep(0.2)
    global QTD_CLIENT_PROCS_COUNTER
    global QTD_SERVER_PROCS_COUNTER
    messages_counter = 0
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(addr[prts])
        server.listen(QTD_CLIENT_PROCS)
        print("Server-{} started in {} and listening...".format(os.getpid(), addr[prts]))

        try:
            while(True):
                time.sleep(1)
                if(messages_counter == QTD_CLIENT_PROCS):
                    break
                #connection, client_addr = server.accept()
                #print("Sever-{} received a connection!".format(os.getpid()))

                while(messages_counter < QTD_CLIENT_PROCS):
                    #connection, client_addr = server.accept()
                    print("Sever-{} received a connection!".format(os.getpid()))
                    message_received = connection.recv(64)
                    if(not message_received):
                        time.sleep(1)
                        break
                    print("Server-{} received {}".format(os.getpid(), message_received))
                    #connection.close()
                    messages_counter += 1
                    print("msg_count_server->{}".format(messages_counter))
                
        except Exception:
            #connection.close()
            print("Err. Sever-{} closed the connection!".format(os.getpid()))
            time.sleep(1)

        finally:
            #connection.close()
            print("Server-{} done".format(os.getpid()))

    except Exception:
        print("Was not possible to create a server!")

    finally:
        print("Server-{} done".format(os.getpid()))


def client_start(num):
    time.sleep(1)
    messages_counter = 0

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client-{} started".format(os.getpid()))
        message = str(num)

        try:
            while(True):
                time.sleep(1)
                if(messages_counter == QTD_SERVER_PROCS):
                    break
                #client.connect(addr[messages_counter])
                while(messages_counter < QTD_SERVER_PROCS):
                    #print("Client-{} sending message to {}".format(os.getpid(), addr[messages_counter]))
                    client.sendto(message.encode(), addr[messages_counter])
                    #time.sleep(1)
                    print("Client-{} send {} for {}".format(os.getpid(), message, addr[messages_counter]))
                    messages_counter += 1
                    print("msg_count_client->{}".format(messages_counter))
                    #client.close()
                    #break
                else:
                    time.sleep(1)

        except Exception:
            client.close()
            print("Err. Client-{} closed the connection!".format(os.getpid()))
            time.sleep(1)

        finally:
            client.close()

    except Exception:
        print("Was not possible to create a lient!")

    finally:
        print("Client-{} done".format(os.getpid()))


#if __name__ == 'main':


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

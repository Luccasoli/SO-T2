import socket
import multiprocessing as mp
import os
import random
import time
#from memory_profiler import profile


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

# Generates numbers between 1 and 100


def rnum():
    return random.randint(1, 100)


# Creates Server Sockets


def server_start(prts):
    messages_counter = 0

    # First try: Server Socket are created and binded to an address
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Use the address port even it is blocked(root requires)
        server.bind(addr[prts]) # Number of messages received before reject new messages
        server.listen(QTD_CLIENT_PROCS)
        print("Server-{} started in {} and listening...".format(os.getpid(), addr[prts]))

        # Second try: Server Socket are able to accept connections from clients and receive their messages
        try:
            while(messages_counter < QTD_CLIENT_PROCS):
                (connection, client_addr) = server.accept()
                message_received = connection.recv(64)
                if(not message_received):
                    break
                print("Server-{} received {} from {}".format(os.getpid(), message_received, client_addr))
                messages_counter += 1
                #connection.close()

        except Exception:
            print("Was not possible to connect/recive in Server-{}".format(os.getpid()))

    except Exception:
        print("Was not possible to create the Server-{}!".format(os.getpid))

    finally:
        connection.close()  # Closes the connection(client socket) between client and server
        print("Server-{} done".format(os.getpid()))


def client_start(num):
    message = str(num)
    messages_counter = 0
    print("")

    # First try: Client Sockets are created
    try:
        client_socks = []
        for i in range(QTD_SERVER_PROCS):
            client_socks.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))    
        print("Client-{} started".format(os.getpid()))

        # Second try: Client Sockets connect in addresses and send a message
        try:
            while(messages_counter < QTD_SERVER_PROCS):
                client_socks[messages_counter].connect(addr[messages_counter])
                client_socks[messages_counter].send(message.encode())
                print("Client-{} send {} for {}".format(os.getpid(), message, addr[messages_counter]))
                messages_counter += 1

        except Exception:
            print("Was not possible to connect/send in Client-{}".format(os.getpid()))
        
    except Exception:
        print("Was not possible to create the Client-{}!".format(os.getpid()))

    finally:
        print("Client-{} done".format(os.getpid()))


@profile
def cinco_cinco():
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
    cinco_cinco()
    print("Time spent: {}".format(time.time() - total_time))

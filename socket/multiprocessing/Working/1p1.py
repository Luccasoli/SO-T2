import socket
import multiprocessing as mp
import os
import random
import time
import queue


## Informations

QTD_SERVER_PROCS = 1
QTD_CLIENT_PROCS = 1
total_time = 0

host = '127.0.0.1'
port = 2426
addr = (host, port)


## Sockets

server_procs = []
client_procs = []


## defs


def rnum():
    return random.randint(1, 100)


def server_start():
    #time.sleep(0.2)
    messages_counter = 0

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(addr)
        server.listen(QTD_CLIENT_PROCS)
        print("Server-{} started in {} and listening...".format(os.getpid(), addr))
    
        try:
            while(messages_counter < QTD_CLIENT_PROCS):
                (connection, client_addr) = server.accept()
                message_received = connection.recv(64)
                if(not message_received):
                    #time.sleep(0.5)
                    break
                print("Server-{} received {} from {}".format(os.getpid(), message_received, client_addr))
                messages_counter += 1
                #print("msg_count_server->{}".format(messages_counter))
        
        except Exception:
            print("Was not possible to connect/recive in Server-{}".format(os.getpid()))
    
    except Exception:
        print("Was not possible to create the Server-{}!".format(os.getpid))

    finally:
        connection.close()
        print("Server-{} done".format(os.getpid()))


def client_start(num):
    #time.sleep(0.4)
    message = str(num)
    print("")

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client-{} started".format(os.getpid()))
    
        try:
            client.connect(addr)
            client.send(message.encode())
            print("Client-{} send {} for {}".format(os.getpid(), message, addr))

        except Exception:
            print("Was not possible to connect/send in Client-{}".format(os.getpid()))

    except Exception:
        print("Was not possible to create the Client-{}!".format(os.getpid()))

    finally:
        print("Client-{} done".format(os.getpid()))


def umpum():
    server_proc = mp.Process(target=server_start)
    server_proc.daemon = True
    client_proc = mp.Process(target=client_start, args=(rnum(), ))
    client_proc.daemon = True
    server_proc.start()
    client_proc.start()
    client_proc.join()
    #server_proc.join()


if __name__ == "__main__":
    total_time = time.time()
    umpum()
    print("\n\nTime spent: {}".format(time.time() - total_time))

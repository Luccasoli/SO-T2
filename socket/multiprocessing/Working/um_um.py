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


## defs

# Generates numbers between 1 and 100    


def rnum():
    return random.randint(1, 100)


# Creates Server Sockets


def server_start():
    messages_counter = 0

    # First try: Server Socket are created and binded to an address
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Use the address port even it is blocked(root requires)
        server.bind(addr)
        server.listen(QTD_CLIENT_PROCS) # Number of messages received before reject new messages
        print("Server-{} started in {} and listening...".format(os.getpid(), addr))
    
        # Second try: Server Socket are able to accept connections from clients and receive their messages
        try:
            while(messages_counter < QTD_CLIENT_PROCS):
                (connection, client_addr) = server.accept() 
                message_received = connection.recv(64)
                if(not message_received):
                    break
                print("Server-{} received {} from {}".format(os.getpid(), message_received, client_addr))
                messages_counter += 1
        
        except Exception:
            print("Was not possible to connect/recive in Server-{}".format(os.getpid()))
    
    except Exception:
        print("Was not possible to create the Server-{}!".format(os.getpid))

    finally:
        connection.close()  # Closes the connection(client socket) between client and server
        print("Server-{} done".format(os.getpid()))


# Creates Client Sockets


def client_start(num):
    message = str(num)
    print("")

    # First try: Client Socket are created
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client-{} started".format(os.getpid()))
    
    # Second try: Client Socket connect in address and send a message
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


def um_um():
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
    um_um()
    print("\n\nTime spent: {}".format(time.time() - total_time))

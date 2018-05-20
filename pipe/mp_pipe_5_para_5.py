import threading, multiprocessing, random, time

def write(pipe, n):
    r, w = pipe
    msg = "Texto"
    for j in range(5):
        number = random.randint(0,100)
        w.send(number)
        print("Mensagem escrita no Pipe {}: {}".format(n, number))
    w.close()
    print("\n")

def reader(pipe, t):
    r, w = pipe
    aux, barrier = t
    l, n = aux
    while True:
        try:
            barrier.wait() # Espera todas as threads chegarem nesse ponto
            l.acquire() # Trava região crítica
            
            msg = r.recv()    # Lê da saída do Pipe
            print("Thread {} recebe: {} do Pipe {}".format(threading.get_ident(), msg, n))
            
        except EOFError:
            break
        except OSError:
            print("OSError")
            break
        finally:
            l.release() # Destrava

def mp_pipe_1_para_5():
    pipes = []
    writers = []
    locks = []
    readers = []
    barriers = []
    for i in range(5):
        pipes.append(multiprocessing.Pipe())
        writers.append(threading.Thread(target=write, args=(pipes[i], i+1)))
        locks.append(threading.Lock())
        readers.append([])
        barriers.append(threading.Barrier(5))
    
    for i in range(5):
        writers[i].start()
        writers[i].join()
        for j in range(5):
            readers[i].append(threading.Thread(target=reader, args=((pipes[i]), ((locks[i], i+1), barriers[i]))))
    
    start = time.time()
    for i in range(5):
        for j in range(5):
            readers[i][j].start() # Executa 5 processos que leem do Pipe

    for i in range(5):
        for j in range(5):
            readers[i][j].join() # Executa 5 processos que leem do Pipe

    print("Tempo de leitura = {}".format(time.time() - start))

if __name__ == "__main__":
    mp_pipe_1_para_5()
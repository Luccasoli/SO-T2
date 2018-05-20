import multiprocessing, os, sys, time, random, threading

def write(pipe):
    r, w = pipe
    msg = "Texto"
    for j in range(5):
        number = random.randint(0,100)
        w.send(number)
        print("Mensagem escrita no Pipe {}".format(number))
    w.close()

def reader(pipe, t):
    r, w = pipe
    l, barrier = t
    while True:
        try:
            barrier.wait() # Espera todas as threads chegarem nesse ponto
            l.acquire() # Trava região crítica
            
            msg = r.recv()    # Lê da saída do Pipe
            print("Thread {} recebe: {}".format(threading.get_ident(), msg))
            
        except EOFError:
            break
        except OSError:
            print("OSError")
            break
        finally:
            l.release() # Destrava

def mp_pipe_1_para_5():
    barrier = threading.Barrier(5) # Entidade de sincronização das threads
    r, w = multiprocessing.Pipe() # Cria um Pipe de comunicação
    writer = threading.Thread(target=write, args=((r, w), )) # A Thread que escreve no Pipe

    writer.start() # Inicia o mesmo

    l = multiprocessing.Lock() # Instancia uma trava

    reader_p = list()

    for i in range(5): # Cria uma lista de processos 
        reader_p.append(threading.Thread(target=reader, args=((r, w), (l, barrier))))

    start = time.time()
    for i in range(5):
        reader_p[i].start() # Executa 5 processos que leem do Pipe

    for i in range(5):
        reader_p[i].join() # Espera as 5 thread concluirem para continuar

    print("Tempo de leitura = {}".format(time.time() - start))

if __name__ == "__main__":
    mp_pipe_1_para_5()
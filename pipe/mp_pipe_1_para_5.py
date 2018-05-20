import multiprocessing, os, sys, time, random, threading

def write(pipe):
    r, w = pipe
    for j in range(5):
        number = random.randint(0,100) # Gera um número aleatório
        w.send(number) # Envia o número para o Pipe
        print("Mensagem escrita no Pipe {}".format(number))
    w.close()

def read(pipe, t):
    r, w = pipe
    l, barrier = t # l = Lock e barrier = Barrier()
    while True:
        try:
            barrier.wait() # Espera todas as Threads chegarem nesse ponto
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
    barrier = threading.Barrier(5) # Entidade de sincronização das Threads
    r, w = multiprocessing.Pipe() # Cria um Pipe de comunicação
    writer = threading.Thread(target=write, args=((r, w), )) # A Thread que escreve no Pipe

    writer.start() # Inicia o mesmo

    l = multiprocessing.Lock() # Instancia uma trava

    reader = []

    for i in range(5): # Cria uma lista de processos 
        reader.append(threading.Thread(target=read, args=((r, w), (l, barrier))))

    start = time.time() # Inicia a contagem do tempo de processamento de leitura
    for i in range(5):
        reader[i].start() # Executa 5 Threads que leem do Pipe

    for i in range(5):
        reader[i].join() # Espera as 5 Threads concluirem para continuar

    print("Tempo de leitura = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura

if __name__ == "__main__":
    mp_pipe_1_para_5()
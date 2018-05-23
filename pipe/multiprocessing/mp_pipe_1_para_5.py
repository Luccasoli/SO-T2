import multiprocessing, os, sys, time, random, threading

def write(pipe):
    r, w = pipe
    for j in range(5):
        number = random.randint(0,100) # Gera um número aleatório
        w.send(number) # Envia o número para o Pipe
        print("Mensagem escrita no Pipe: {} pelo processo {}".format(number, os.getpid()))


def read(pipe, t):
    r, w = pipe
    lock, barrier = t # l = Lock e barrier = Barrier()
    w.close() # Fecha a escrita no Pipe

    try:
        barrier.wait() # Espera todas as Processs chegarem nesse ponto
        lock.acquire() # Trava região crítica
        msg = r.recv()    # Lê da saída do Pipe
        print("Process {} recebe: {}".format(os.getpid(), msg))
        
    except EOFError:
        pass
    except OSError:
        print("OSError")
        
    finally:
        lock.release() # Destrava
            

def mp_pipe_1_para_5():
    barrier = multiprocessing.Barrier(5) # Entidade de sincronização das Processs
    r, w = multiprocessing.Pipe() # Cria um Pipe de comunicação
    writer = multiprocessing.Process(target=write, args=((r, w), )) # A Process que escreve no Pipe

    writer.start() # Inicia o mesmo

    lock = multiprocessing.Lock() # Instancia uma trava

    reader = []

    for i in range(5): # Cria uma lista de processos 
        reader.append(multiprocessing.Process(target=read, args=((r, w), (lock, barrier))))

    start = time.time() # Inicia a contagem do tempo de processamento de leitura
    for i in range(5):
        reader[i].start() # Executa 5 Processs que leem do Pipe

    for i in range(5):
        reader[i].join() # Espera as 5 Processs concluirem para continuar

    print("Tempo de leitura = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura

if __name__ == "__main__":
    mp_pipe_1_para_5()
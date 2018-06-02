import multiprocessing, os, sys, time, random, threading
from memory_profiler import profile

lock_shared = multiprocessing.Lock() # Garante a ordem correta dos "prints"

def write(*pipes):

    try:
        for i in range(5): # Escreve uma vez em cada Pipe
            number = random.randint(0, 100) # Gera um número aleatório entre 0 e 99
            pipe, numero_pipe = pipes[i]
            r, w = pipe # Variáveis de acesso ao Pipe
            r.close() # Bloqueia leitura no Pipe

            lock_shared.acquire() # Abre trava
            w.send(number) # Envia o número para o Pipe
            print("+ Mensagem escrita no Pipe {}: {} pelo processo {}".format(numero_pipe, number, os.getpid()))
            lock_shared.release() # Fecha trava
    except EOFError:
        pass
    except OSError:
        print("OSError")
            

def read(*pipes):

    pipe, numero_pipe = pipes
    r, w = pipe # Variáveis de acesso ao Pipe
    w.close() # Bloqueia a escrita no Pipe

    try:
        for i in range(5):
            msg = r.recv()    # Lê da saída do Pipe
            lock_shared.acquire()
            print("- Processo {} recebe do pipe {} na posição {}: {}".format(os.getpid(), numero_pipe, i+1, msg))
            lock_shared.release()
    except EOFError:
        pass
    except OSError:
        print("OSError")
            

def mp_pipe_1_para_5():

    # Declaração de listas
    pipes = list()
    writers = list()
    readers = list()

    for i in range(5):
        pipes.append((multiprocessing.Pipe(), i+1)) # Cria 5 Pipes

    for i in range(5):
        writers.append(multiprocessing.Process(target=write, args=(pipes))) # Cria 5 Processos em que cada 1 escreve 1 número em cada Pipe
        readers.append(multiprocessing.Process(target=read, args=(pipes[i]))) # Cria 5 Processos em que cada 1 lê 5 números de cada Pipe

    
    for i in range(5):
        writers[i].start() # Inicializa os 5 processos de escrevem nos Pipes
        readers[i].start() # Inicializa os 5 processos de leem dos Pipes

    for i in range(5): # Garante que a "main" não vai concluir antes dos Processos
        writers[i].join() 
        readers[i].join()


if __name__ == "__main__": 
    start = time.time() # Inicia a contagem do tempo de processamento de leitura
    mp_pipe_1_para_5() 
    print("Tempo de execução = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura
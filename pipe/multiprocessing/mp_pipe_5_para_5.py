import multiprocessing, multiprocessing, random, time, os

def write(pipe, n):
    r, w = pipe
    for j in range(5):
        number = random.randint(0,100) # Gera um número aleatório
        w.send(number) # Envia o número para o Pipe
        print("Mensagem escrita no Pipe {}: {}".format(n, number))
    w.close() # Bloqueia escritas no Pipe
    print("\n")

def read(pipe, t):
    r, w = pipe
    aux, barrier = t
    l, n = aux # l = Lock e n = Número do Pipe
    w.close()

    try:
        barrier.wait() # Espera todas as Processs chegarem nesse ponto
        l.acquire() # Trava região crítica
        
        msg = r.recv()    # Lê da saída do Pipe
        print("Process {} recebe: {} do Pipe {}".format(os.getpid(), msg, n))
        
    except EOFError:
        pass
    except OSError:
        print("OSError")
        
    finally:
        l.release() # Destrava

def mp_pipe_1_para_5():
    pipes = []
    writers = []
    locks = []
    readers = []
    barriers = []
    for i in range(5):
        pipes.append(multiprocessing.Pipe()) # Cria os Pipes de comunicação
        writers.append(multiprocessing.Process(target=write, args=(pipes[i], i+1))) # As Processs que vão escrever em cada Pipe
        locks.append(multiprocessing.Lock()) # Entidades de sincronização das Processs
        readers.append([]) # Cria uma lista em cada variável
        barriers.append(multiprocessing.Barrier(5)) # Entidades de sincronização das Processs
    
    for i in range(5):
        writers[i].start() # Inicia as Processs que escrevem nos Pipes
        writers[i].join() # Aguarda cada uma concluir sua escrita
        for j in range(5):
            readers[i].append(multiprocessing.Process(target=read, args=((pipes[i]), ((locks[i], i+1), barriers[i])))) # Adiciona 5 Processs de Leitura para cada Pipe
    
    start = time.time() # Inicia a contagem do tempo de processamento de leitura
    for i in range(5):
        for j in range(5):
            readers[i][j].start() # Executa 5 Processs que leem de cada um dos 5 Pipes

    for i in range(5):
        for j in range(5):
            readers[i][j].join() # Aguarda cada Process de leitura concluir

    print("Tempo de leitura = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura

if __name__ == "__main__":
    mp_pipe_1_para_5()
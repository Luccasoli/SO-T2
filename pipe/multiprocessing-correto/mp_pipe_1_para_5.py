import multiprocessing, os, sys, time, random, threading

lock_shared = multiprocessing.Lock() # Garante a ordem correta dos "prints"

def write(*pipe):

    r, w = pipe # Variáveis de acesso ao Pipe
    r.close() # Fecha a leitura no Pipe

    try:
        number = random.randint(0,100) # Gera um número aleatório
        
        lock_shared.acquire() # Abre trava
        w.send(number) # Envia o número para o Pipe
        print("Mensagem escrita no Pipe: {} pelo processo {}".format(number, os.getpid()))
        lock_shared.release() # Fecha trava
    except EOFError:
        pass
    except OSError:
        print("OSError")


def read(*pipe):

    r, w = pipe # Variáveis de acesso ao Pipe
    w.close() # Fecha a escrita no Pipe

    try:
        for i in range(5):
            msg = r.recv() # Lê da saída do Pipe
            lock_shared.acquire()
            print("Processo {} recebe: {}".format(os.getpid(), msg))
            lock_shared.release()
    except EOFError:
        pass
    except OSError:
        print("OSError")


def mp_pipe_1_para_5():

    r, w = multiprocessing.Pipe() # Cria um Pipe de comunicação

    writers = list()

    for i in range(5):
        writers.append(multiprocessing.Process(target=write, args=(r, w))) # Cria 5 Processos em que cada 1 escreve 1 número no Pipe
    
    for i in range(5):
        writers[i].start() # Inicializa os 5 Processos de escrevem no Pipe

    reader = multiprocessing.Process(target=read, args=(r, w)) # Cria 1 Processo que lê 5 números do Pipe

    reader.start() # Inicializa o Processe que lê do Pipe

    # Garante que a "main" não vai concluir antes dos Processos
    for i in range(5):
        writers[i].join
    reader.join() 



if __name__ == "__main__":
    start = time.time() # Inicia a contagem do tempo de processamento de leitura
    mp_pipe_1_para_5()
    print("Tempo de execução = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura
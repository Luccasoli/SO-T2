import multiprocessing, os, random, time
from memory_profiler import profile

def write(*pipe):

    r, w = pipe # Variáveis de acesso ao Pipe
    r.close() # Fecha a leitura do Pipe

    try:
        number = random.randint(0,100) # Gera um número aleatório
        w.send(number) # Envia o número para o Pipe
        print("Mensagem escrita no Pipe: {} pelo processo {}".format(number, os.getpid()))
    except EOFError:
        pass
    except OSError:
        print("OSError")

def read(*pipe):

    r, w = pipe # Variáveis de acesso ao Pipe
    w.close() # Fecha a escrita no Pipe

    try:
        msg = r.recv() # Lê da saída do Pipe
        print("Processo {} recebe: {}".format(os.getpid(), msg))
    except EOFError:
        pass
    except OSError:
        print("OSError")

@profile(precision=10)
def mp_pipe_1_para_1():

    r, w = multiprocessing.Pipe() # Cria um Pipe de comunicação

    writer = multiprocessing.Process(target=write, args=(r, w)) # Cria o Processo que escreve no Pipe
    writer.start() # Inicia o Processo que escreve no Pipe

    reader = multiprocessing.Process(target=read, args=(r, w)) # Cria o Processo que lê do Pipe
    reader.start() # Inicia o Processo que lê do Pipe
    
    writer.join() # Aguarda o Processo terminar de escrever
    reader.join() # Aguarda o Processo terminar de ler
    

if __name__ == "__main__":
    start = time.time() # Inicia a contagem do tempo de processamento de leitura
    mp_pipe_1_para_1()
    print("Tempo de leitura = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura
import multiprocessing, os, random, time, threading

def write(pipe):
    r, w = pipe
    number = random.randint(0,100) # Gera um número aleatório
    w.send(number) # Envia o número para o Pipe
    print("Mensagem escrita no Pipe: {}".format(number))
    w.close() # Bloqueia escritas no Pipe

def read(pipe):
    r, w = pipe
    while True:
        try:
            msg = r.recv()    # Lê da saída do Pipe
            print("Thread {} recebe: {}".format(threading.get_ident(), msg))
            
        except EOFError:
            break
        except OSError:
            print("OSError")
            break

def mp_pipe_1_para_1():
    r, w = multiprocessing.Pipe() # Cria um Pipe de comunicação

    writer = threading.Thread(target=write, args=((r, w), )) # Cria a Thread que escreve no Pipe
    writer.start() # Inicia a Thread que escreve no Pipe
    writer.join() # Aguarda a Thread terminar de escrever

    start = time.time() # Inicia a contagem do tempo de processamento de leitura

    reader = threading.Thread(target=read, args=((r, w), )) # Cria a Thread que lê do Pipe
    reader.start() # Inicia a Thread que lê do Pipe
    reader.join() # Aguarda a Thread terminar de ler

    print("Tempo de leitura = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura

if __name__ == "__main__":
    mp_pipe_1_para_1()
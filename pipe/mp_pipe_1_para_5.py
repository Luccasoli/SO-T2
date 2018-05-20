import multiprocessing, os, sys, time, random, threading

def write(pipe):
    r, w = pipe
    msg = "Texto"
    for j in range(5):
        w.send(random.randint(0,100))
        print("Mensagem escrita no Pipe")
    w.close()

def readers(pipe, l):
    r, w = pipe
    while True:
        try:
            l.acquire() # Trava região crítica
            msg = r.recv()    # Lê da saída do Pipe
            print("Processo {} recebe: {}\te retorna o inverso: {}".format(os.getpid(), msg, msg))
            
        except EOFError:
            break
        except OSError:
            print("OSError")
            break
        finally:
            l.release()

def mp_pipe_1_para_5():
    r, w = multiprocessing.Pipe() # Cria um Pipe de comunicação
    writer = threading.Thread(target=write, args=((r, w), ))

    #writer = multiprocessing.Process(target=write, args=((r, w),)) # Processo que escreve no Pipe
    writer.start() # Inicia o mesmo
    #w.close() # Bloqueia escritas no Pipe

    l = multiprocessing.Lock() # Instancia uma trava

    reader_p = list()

    for i in range(5): # Cria uma lista de processos
        #reader_p.append(multiprocessing.Process(target=readers, args=((r, w),l))) 
        reader_p.append(threading.Thread(target=readers, args=((r, w), l))) 

    for i in range(5):
        reader_p[i].start() # Executa 5 processos que leem do Pipe

if __name__ == "__main__":
    mp_pipe_1_para_5()
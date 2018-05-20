import multiprocessing, os

def mp_pipe_1_para_1():
    # Cria um Pipe
    r, w = multiprocessing.Pipe()

    if(os.fork() == 0):
        # Processo Pai
        r.close() # Fecha a leitura no Pipe
        msg = "Texto" 
        print("Processo Pai envia: {}".format(msg))
        w.send(msg) # Escreve no Pipe

    else:
        # Processo Filho
        w.close() # Fecha a escrita no Pipe
        msg = r.recv() # Lê do Pipe
        print("Processo Filho recebe: {}\tE retorna o inverso: {}".format(msg, msg[::-1]))

if __name__ == "__main__":
    mp_pipe_1_para_1()
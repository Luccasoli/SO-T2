
import os
from multiprocessing import Process, Value #importacoes para usar processos e memoria compartilhada
import random
import time
from memory_profiler import profile

@profile
def main():
    def gera_num():
        return random.randint(1, 100)#funcao para gerar mensagem entre 1 e 100
    
    myVar= [] #lista vazia
    
    for i in range (5):
        myVar.append(Value("i", gera_num()))#acrescentando na lista

    def funcaoFilho():
        print (". (PID=" + str(os.getpid())+"). Mensagem para filho: "+ str(myVar[i].value)) #gera a mensagem aleatoria
    
    def funcaoLeitura():
        for i in range (5):
            print (". (PID=" + str(os.getpid())+"). Mensagem do pai: "+ str(myVar[i].value))    #ler a mensagem

    for i in range(5):
        newP = Process(target=funcaoFilho) #criacao dos processos para chamar a funcaoFilho
        newP.start()
        newP.join()
        
    for i in range(5):
        newP = Process(target=funcaoLeitura) #criacao dos processo para chamar a funcaoleitura
        newP.start()
        newP.join()


if __name__ == "__main__":
    start = time.time() # Inicia a contagem do tempo de processamento de leitura
    main()
    print("Tempo de leitura = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura
import os
import time
from multiprocessing import Process, Value #importacoes para usar processos e memoria compartilhada
import random
from memory_profiler import profile

@profile
def main():
    def gera_num():
        return random.randint(1, 100) #funcao para gerar numero aleatorio

    myVar = [] #lista vazia
    
    def funcaoFilho():
        print (". (PID=" + str(os.getpid())+"). Mensagem para filho: "+ str(myVar[i].value)) #funcao que envia a mensagem


    def funcaoLeitura():
        for i in range (5):
            print (". (PID=" + str(os.getpid())+"). Mensagem do pai: "+ str(myVar[i].value))    #funcao que le a mensagem


    for i in range (5):
        myVar.append(Value("i", gera_num())) # Acrescenta na lista o numero gerado pela funcao


    for i in range(5):
        newP = Process(target=funcaoFilho) #criacao dos 5 processos para chamar a funcaoFilho
        newP.start()
        newP.join()
        
    newP = Process(target=funcaoLeitura) #criacao do processo para chamar a funcaoleitura
    newP.start()
    newP.join()
    

if __name__ == "__main__":
    start = time.time() # Inicia a contagem do tempo de processamento de leitura
    main()
    print("Tempo de leitura = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura
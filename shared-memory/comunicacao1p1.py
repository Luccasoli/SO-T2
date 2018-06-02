import os
from multiprocessing import Process, Value #importacoes para usar processos e memoria compartilhada
import random
import time
from memory_profiler import profile

@profile
def main():
    def gera_num():
        return random.randint(1, 100) #funcao para gerar numero aleatorio

    def funcaoFilho():
        print ("Filho - (PID=" + str(os.getpid())+"). Mensagem do pai: "+ str(myVar.value))

    myVar = Value("i", gera_num()) #variavel compartilhada usada pelos processos

    print("Pai - (PID=" + str(os.getpid())+"). Mensagem para filho: "+ str(myVar.value))

    newP = Process(target=funcaoFilho) # Criação do processo chamando a funcaoFilho
    newP.start()
    newP.join()
    
    
if __name__ == "__main__":
    start = time.time() # Inicia a contagem do tempo de processamento de leitura
    main()
    print("Tempo de leitura = {}".format(time.time() - start)) # Exibe a duração do tempo de leitura
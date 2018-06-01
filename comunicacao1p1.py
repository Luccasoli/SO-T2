
import os
from multiprocessing import Process, Value #importacoes para usar processos e memoria compartilhada
import random

def gera_num():
    return random.randint(1, 100) #funcao para gerar numero aleatorio



myVar = Value("i", gera_num()) #variavel compartilhada usada pelos processos

def funcaoFilho():
    
    print (". (PID=" + str(os.getpid())+"). Mensagem do pai: "+ str(myVar.value))
    

print (". (PID=" + str(os.getpid())+"). Mensagem para filho: "+ str(myVar.value))

newP = Process(target=funcaoFilho) #criacao do processo chamando a funcaoFilho
newP.start()
newP.join()


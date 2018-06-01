
import os
from multiprocessing import Process, Value #importacoes para usar processos e memoria compartilhada
import random
@profile
def gera_num():
    return random.randint(1, 100) #funcao para gerar numero aleatorio

 
myVar= [] #lista vazia
 
for i in range (5):
    myVar.append(Value("i", gera_num())) #acrescenta na lista o numero gerado pela funcao
def funcaoFilho():
   
    print (". (PID=" + str(os.getpid())+"). Mensagem para filho: "+ str(myVar[i].value)) #funcao que envia a mensagem
def funcaoLeitura():
    for i in range (5):
   	 print (". (PID=" + str(os.getpid())+"). Mensagem do pai: "+ str(myVar[i].value))    #funcao que le a mensagem

for i in range(5):
    newP = Process(target=funcaoFilho) #criacao dos 5 processos para chamar a funcaoFilho
    newP.start()
    newP.join()
    
for i in range(1):
    newP = Process(target=funcaoLeitura) #criacao do processo para chamar a funcaoleitura
    newP.start()
    newP.join()


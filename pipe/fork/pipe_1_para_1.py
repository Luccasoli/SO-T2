import os



def pipe_1_para_1():
    r, w = os.pipe()
    aux = os.fork()
    if(aux):
        # Processo pai:
        os.close(r)
        print("Processo pai")
        w = os.fdopen(w, 'w')
        msg = "Texto"
        w.write(msg)
        print("Pai envia: {}".format(msg))
        w.close()

    
    else:
        # Processo filho:
        os.close(w)
        print("Processo filho")
        r = os.fdopen(r)
        str = r.read()
        print("Filho recebe {} e escreve: {}".format(str, str[::-1]))
        r.close()
    

if __name__ == '__main__':
    pipe_1_para_1()
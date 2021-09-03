#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

imageR="img/imagem.png"
imageW="img/imagemCopia.png"




def cria_sequencia():
    tamanho=random.randint(10,30)
    comandos=[(255).to_bytes(2, byteorder='big'),(0).to_bytes(1, byteorder='big'),(15).to_bytes(1, byteorder='big'),(240).to_bytes(1, byteorder='big'),(65280).to_bytes(2, byteorder='big'),(255).to_bytes(1, byteorder='big')]
    lista=[0]*(tamanho+1)
    for i in range (tamanho):
        com=random.choice(comandos)
        if len(com)==2:
            com=(int.from_bytes(com, byteorder='big')+131072).to_bytes(3, byteorder='big')
        lista[i+1]=com
    lista[0]=(170).to_bytes(1, byteorder='big')
    lista.append((1).to_bytes(1, byteorder='big'))
    return lista,tamanho

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM3')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print ('Comunicação aberta')
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.

        #txBuffer: sequência de comandos a ser enviado para o outro computador.
        
        seq,tam=cria_sequencia()
        i=1
        for comand in seq:
        
            print ('Transmissão do comando {} começando'.format(i))
            txBuffer=comand
            print ('Enviando {}'.format(txBuffer))
            com1.sendData(np.asarray(txBuffer))
            i+=1
            time.sleep(0.2)
        print ("Comandos enviados pelo cliente: {}".format(tam))
        rxBuffer,nRx=com1.getData(1)
        print ("Comandos recebidos pelo servidor: {}".format(int.from_bytes(rxBuffer, byteorder='big')))
        
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

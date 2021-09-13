#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from threading import Timer
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

imageR="imagem.png"
imageW="img/imagemCopia.png"




txBuffer=(255).to_bytes(114*2+10, byteorder='big')

def calcula_quant(tamanho):
    if tamanho%114==0:
        return tamanho//114
    else:
        return tamanho//114 + 1

def cria_head(n_atual,n_total,n_bytespay):
    head=[0]*10
    head[0]=(170).to_bytes(1, byteorder='big')
    head[1]=(n_atual).to_bytes(1, byteorder='big')
    head[2]=(n_total).to_bytes(1, byteorder='big')
    head[3]=(n_bytespay).to_bytes(1, byteorder='big')
    head[4]=(170).to_bytes(1, byteorder='big')
    head[5]=(170).to_bytes(1, byteorder='big')
    head[6]=(170).to_bytes(1, byteorder='big')
    head[7]=(170).to_bytes(1, byteorder='big')
    head[8]=(170).to_bytes(1, byteorder='big')
    head[9]=(170).to_bytes(1, byteorder='big')
    
    return head

def cria_lista(binario):
    lista=[]
    for bit in binario:
        lista.append((bit).to_bytes(1, byteorder='big'))
    return lista

def cria_datagrama(arquivo):
    #Retorna uma lista de datagramas (cada elemento é uma lista de bygtes com head, payload e eop) a partir de um arquivo
    bytes=cria_lista(arquivo)
    payload=114
  
    quant_pay=calcula_quant(len(arquivo))+1
    lista_datagramas=[0]*quant_pay
    i=0
    for datagrama in range(quant_pay):

        if i==0:
            head=cria_head(0,quant_pay,0)
            bytes_pay=[]
        elif i!=quant_pay-1:
            #Se não é o último pacote
            head=cria_head(i+1,quant_pay,payload)
            bytes_pay=[0]*payload
            for quant in range(payload):
                bytes_pay[quant]=bytes.pop(0)
        
        else:
            #Se é o último pacote
            head=cria_head(i+1,quant_pay,len(arquivo)%payload)
            bytes_resto=(len(arquivo))%payload
            bytes_pay=[0]*bytes_resto
            for quant in range(bytes_resto):
                bytes_pay[quant]=bytes.pop(0)

        eop=[(170).to_bytes(1, byteorder='big')]*3
        eop.append((204).to_bytes(1, byteorder='big'))
        data=head+bytes_pay+eop
        lista_datagramas[i]=data
        i+=1
    return lista_datagramas


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
        
        # seq,tam=cria_sequencia()
        # i=1
        # for comand in seq:
        
        #     print ('Transmissão do comando {} começando'.format(i))
        #     txBuffer=comand
        #     print ('Enviando {}'.format(txBuffer))
        #     com1.sendData(np.asarray(txBuffer))
        #     i+=1
        #     time.sleep(0.2)
        # print ("Comandos enviados pelo cliente: {}".format(tam))
        # rxBuffer,nRx=com1.getData(1)
        # print ("Comandos recebidos pelo servidor: {}".format(int.from_bytes(rxBuffer, byteorder='big')))
        
        datagramas=cria_datagrama(txBuffer)
        hand=True
        print ("Iniciando o Handshake")
        com1.sendData(np.asarray(datagramas[0]))
        print ("Enviando {}".format(datagramas[0]))
        # t=Timer(5.0,timeout)
        # t.start()

        seconds_to_go_for = 5 # How long the timer will go for
        current_time = int(time.time()) # Gets the time before the timer starts


        while hand:
            rxBuffer,nRx=com1.getData(14)
            print(rxBuffer)
            if rxBuffer==(255).to_bytes(1, byteorder='big'):
                res=input("Reenviar: S/N")
                if res=="S":
                    print ("Reenviando o Handshake")
                    com1.sendData(np.asarray(datagramas[0]))
                    
                else:
                    hand=False
                    programa=False
            
            else:
                hand=False
                programa=True
                print("Recebeu confirmação")
            
            
        print (programa)
        # while programa:

        


        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

   # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

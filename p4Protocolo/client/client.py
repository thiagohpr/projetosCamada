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

eop1=b'\xaa'
eop2=b'\xff'
eop=[eop2,eop1,eop2,eop1]

def calcula_quant(tamanho):
    if tamanho%114==0:
        return tamanho//114
    else:
        return tamanho//114 + 1

def cria_head(tipo,n_atual,n_total,n_bytespay):
    head=[0]*10
    head[0]=(tipo).to_bytes(1, byteorder='big')
    head[1]=(0).to_bytes(1, byteorder='big')#id sensor
    head[2]=(0).to_bytes(1, byteorder='big')#id servidor
    head[3]=(n_total).to_bytes(1, byteorder='big')
    head[4]=(n_atual).to_bytes(1, byteorder='big')
    if tipo==1:
        #id arquivo em handshake
        head[5]=(0).to_bytes(1, byteorder='big')
    else:
        #tamanho do payload
        head[5]=(n_bytespay).to_bytes(1, byteorder='big')
    head[6]=(0).to_bytes(1, byteorder='big')
    head[7]=(170).to_bytes(1, byteorder='big')
    head[8]=(170).to_bytes(1, byteorder='big')
    head[9]=(170).to_bytes(1, byteorder='big')
    return head

def atualiza_head (pacote, cont):
    pacote[7]=cont
    return pacote
def cria_lista(binario):
    lista=[]
    for bit in binario:
        lista.append((bit).to_bytes(1, byteorder='big'))
    return lista

def cria_datagrama(arquivo):
    #Retorna uma lista de datagramas (cada elemento é uma lista de bygtes com head, payload e eop) a partir de um arquivo
    bytes=cria_lista(arquivo)
    payload=114
  
    quant_pay=calcula_quant(len(arquivo))
    lista_datagramas=[0]*(quant_pay+1)
    i=0
    for datagrama in range(quant_pay+1):

        if i==0:
            head=cria_head(1,0,quant_pay,0)
            bytes_pay=[]
        elif i!=quant_pay:
            #Se não é o último pacote
            head=cria_head(3,i,quant_pay,payload)
            bytes_pay=[0]*payload
            for quant in range(payload):
                bytes_pay[quant]=bytes.pop(0)
        
        else:
            #Se é o último pacote
            head=cria_head(i,quant_pay,len(arquivo)%payload)
            bytes_resto=(len(arquivo))%payload
            bytes_pay=[0]*bytes_resto
            for quant in range(bytes_resto):
                bytes_pay[quant]=bytes.pop(0)

        
        
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

        txBuffer=(255).to_bytes(114*2+10, byteorder='big')
        datagramas=cria_datagrama(txBuffer)
        numPck=datagramas[0][3]
        inicia=False
        encerrar=False
        while not inicia:
            #envia mensagem t1
            print("Iniciando Handshake")
            txBuffer=datagramas[0]
            com1.sendData(np.asarray(txBuffer))
            time.sleep(5)
            rxBuffer,nRx=com1.getData(14)
            if rxBuffer[0]==2:
            #se recebeu ok:
                print("Cliente recebeu mensagem de confirmação.")
                inicia=True
                cont=1
            else:
                print("Cliente não recebeu a confirmação.")
        while cont<=numPck:
            #envia pckg cont (mensagem t3)
            print("Enviando pacote {}.".format(cont))
            txBuffer=datagramas[cont]
            com1.sendData(np.asarray(txBuffer))
            startTimer2 = int(time.time())

            recebeuConf=False
            while not recebeuConf:
                if not encerrar:
                    rxBuffer,nRx=com1.getData(14)
                    if rxBuffer[0]==4:
                        #se recebeu mensagem t4 (confirmação do server):
                        print("Recebeu confirmação do servidor.")
                        datagramas[cont+1]=atualiza_head(datagramas[cont+1],cont)
                        cont+=1
                        recebeuConf=True
                    else:
                        #estourou timer 1
                        if rxBuffer==(255).to_bytes(1, byteorder='big'):
                            #reenviar pckg cont (mensagem t3)
                            #reset Timer1
                            print("Timer 1 estourado. Reenviando pacote {}.".format(cont))
                            txBuffer=datagramas[cont]
                            com1.sendData(np.asarray(txBuffer))
                        time_now = int(time.time())
                        if time_now >= startTimer2 + 20:
                            print("Timer 2 encerrado. Timeout de envio do arquivo, finalizando a comunicação.")
                            msgTipo5=cria_head(5,cont,numPck,0)
                            msgTipo5=msgTipo5+eop
                            com1.sendData(np.asarray(msgTipo5))
                            encerrar=True
                        else:
                            rxBuffer,nRx=com1.getData(14)
                            if rxBuffer[0]==6:
                                print("Erro no número do pacote.")
                                #corrigir cont
                                cont=rxBuffer[6]
                                txBuffer=datagramas[cont]
                                com1.sendData(np.asarray(txBuffer))
                                startTimer2 = int(time.time())
                else:
                    break
            if encerrar==True:
                break



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




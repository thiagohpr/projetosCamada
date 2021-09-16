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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)

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
    head[4]=(0).to_bytes(1, byteorder='big')
    head[5]=(0).to_bytes(1, byteorder='big')
    head[6]=(0).to_bytes(1, byteorder='big')
    head[7]=(0).to_bytes(1, byteorder='big')
    head[8]=(0).to_bytes(1, byteorder='big')
    head[9]=(0).to_bytes(1, byteorder='big')
    
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
  
    quant_pay=calcula_quant(len(arquivo))
    lista_datagramas=[0]*quant_pay
    i=0
    for datagrama in range(quant_pay):
        if i!=quant_pay-1:
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

        eop=[(170).to_bytes(1, byteorder='big')]*4
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
        print("comunicacao aberta")
        rxBuffer = 0
        lista = []

        while  rxBuffer != (204).to_bytes(1, byteorder='big'):
            rxBuffer, nRx = com1.getData(1)
            print(rxBuffer)
            lista.append(rxBuffer)
            time.sleep(0.05)
        
        com1.sendData(np.asarray(lista))
        print(lista)
        print('inicando leitura dos pacotes')

        if int.from_bytes(lista[0], byteorder='big') == 170:
            pacotes = int.from_bytes(lista[2], byteorder='big')
        else:
            pacotes = int.from_bytes(lista[1], byteorder='big')


        datagrama = []
        for i in range(pacotes):
            datagrama.append([])
            
        
        i=0
        while i != pacotes:
            rxBuffer, nRx = com1.getData(1)
            datagrama[i].append(rxBuffer)
            time.sleep(0.05)
            print(rxBuffer)
            if rxBuffer == (204).to_bytes(1, byteorder='big'):
                print(datagrama[i])
                time.sleep(4)
                if i>=1:
                    print (int.from_bytes(datagrama[i][1], byteorder='big'))
                    print(int.from_bytes(datagrama[i-1][1], byteorder='big'))
                    if int.from_bytes(datagrama[i][1], byteorder='big') == int.from_bytes(datagrama[i-1][1], byteorder='big') + 1:
                        print('número de pacote correto')
                        if len(datagrama[i]) == int.from_bytes(datagrama[i][3], byteorder='big') + 14:
                            print('número de bytes correto')
                            com1.sendData((100).to_bytes(1, byteorder='big'))
                            i+=1
                            time.sleep(0.1)
                        else: 
                            print('número de bytes incorreto')
                            com1.sendData((101).to_bytes(1, byteorder='big'))
                            datagrama[i]=[]
                    else:
                        print('número de pacote incorreto')
                        com1.sendData((101).to_bytes(1, byteorder='big'))
                        datagrama[i]=[]
                
                else:
                    if len(datagrama[i]) == int.from_bytes(datagrama[i][3], byteorder='big') + 14:
                        print('número de bytes correto')
                        com1.sendData((100).to_bytes(1, byteorder='big'))
                        i+=1
                        time.sleep(0.1)
                    else: 
                        print('número de bytes incorreto')
                        com1.sendData((101).to_bytes(1, byteorder='big'))
                        datagrama[i]=[]
                    

                

        print(datagrama)
        com1.disable()
    
            

                
                

        
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

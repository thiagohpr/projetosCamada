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

meu_id=0
def cria_head(tipo,n_atual,n_total,n_bytespay):
    id_servidor=0
    head=[0]*10
    head[0]=(tipo).to_bytes(1, byteorder='big')
    head[1]=(0).to_bytes(1, byteorder='big')#id sensor
    head[2]=(id_servidor).to_bytes(1, byteorder='big')#id servidor
    head[3]=(n_total).to_bytes(1, byteorder='big')
    head[4]=(n_atual).to_bytes(1, byteorder='big')
    if tipo==1:
        #id arquivo em handshake
        head[5]=(0).to_bytes(1, byteorder='big')

    else:
        #tamanho do payload
        head[5]=(n_bytespay).to_bytes(1, byteorder='big')
    head[6]=(n_atual).to_bytes(1, byteorder='big')
    head[7]=(170).to_bytes(1, byteorder='big')
    head[8]=(170).to_bytes(1, byteorder='big')
    head[9]=(170).to_bytes(1, byteorder='big')
    return head

def cria_log(formato,head):
    
    tipo=str(int.from_bytes(head[0], byteorder='big'))
    tamanho_total=str(int.from_bytes(head[5], byteorder='big')+14)
    linha=time.ctime()+" / "+formato+" / "+tipo+" / "+tamanho_total
    if tipo == '3':
        crc=(hex(int.from_bytes(head[8], byteorder='big'))[2:]+hex(int.from_bytes(head[9], byteorder='big'))[2:]).upper()
        linha+=" / "+str(int.from_bytes(head[4], byteorder='big'))+" / "+str(int.from_bytes(head[3], byteorder='big'))+" / "+crc
    return linha

def log_envio(head):
    with open("C:/Users/thpro/Desktop/Camada Física/projetosCamada/p4Protocolo/server/log.txt", "a") as file:
        file.write(cria_log("envio",head))
        file.write('\n')
def log_recebeu(head):
    with open("C:/Users/thpro/Desktop/Camada Física/projetosCamada/p4Protocolo/server/log.txt", "a") as file:
        file.write(cria_log("receb",head))
        file.write('\n')
def cria_lista(binario):
    lista=[]
    for bit in binario:
        lista.append((bit).to_bytes(1, byteorder='big'))
    return lista
eop1=b'\xaa'
eop2=b'\xff'
eop_fixo=[eop2,eop1,eop2,eop1]

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM3')
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        with open("C:/Users/thpro/Desktop/Camada Física/projetosCamada/p4Protocolo/server/log.txt", "w") as file:
            file.write("Comunicação aberta")
            file.write('\n')
        print("Comunicacao aberta")
        encerrar=False
        ocioso = True
        startTimer2 = int(time.time())
        while ocioso:
            rxBuffer, nRx = com1.getData(14)
            if rxBuffer[0] == 1:
                print("mensagem certa")
                if rxBuffer[2]==meu_id:
                    log_recebeu(cria_lista(rxBuffer))
                    print("é pra mim")
                    ocioso = False
                    numPckg = rxBuffer[3]
                    print("numero certo")
                    cont = 1
                    cont_anterior=0
                    msgTipo2=cria_head(2,cont,numPckg,0)
        
                    msgTipo2=msgTipo2+eop_fixo
                    print(msgTipo2)
                    com1.sendData(np.asarray(msgTipo2))
                    log_envio(msgTipo2)
            else:
                time_now = int(time.time())
                if time_now >= startTimer2 + 20:
                    ocioso = True
                    msgTipo5=cria_head(5,0,0,0)
                    msgTipo5=msgTipo5+eop_fixo 
                    com1.sendData(np.asarray(msgTipo5))
                    log_envio(msgTipo5)
                    encerrar=True
            if encerrar==True:
                break
            time.sleep(1)
        

        if encerrar==False:
            arquivo=[0]*numPckg
            while cont <= numPckg:
                recebeu = False
                seconds_to_go_for = 20
                timer2 = int(time.time())

                while not recebeu:
                    if encerrar==False:
                        head, headn = com1.getData(10)
                        print(head)
                        if len (head)>1:
                            payload, payloadn = com1.getData(head[5])
                            print(payload)
                            eop, eopn = com1.getData(4)
                            print(eop)
                        if head[0] == 3:
                            recebeu = True
                            log_recebeu(cria_lista(head))
                            print("mensagem certa")
                            print (head[7])
                            if head[4] == head[7] + 1:
                                if head[4]==cont_anterior+1:
                                    if len(payload) == head[5]:
                                        arquivo[cont-1] = payload
                                        cont_anterior=cont
                                        msgTipo4=cria_head(4,cont,numPckg,0)
                                        msgTipo4=msgTipo4+eop_fixo

                                        com1.sendData(np.asarray(msgTipo4))
                                        log_envio(msgTipo4)
                                        cont+=1
                                        print("enviando confirmação")
                                        print(cont)
                                        print(numPckg)
                                    else:
                                        msgTipo6=cria_head(6,cont,numPckg,0)
                                        msgTipo6=msgTipo6+eop_fixo 
                                        com1.sendData(np.asarray(msgTipo6))
                                        log_envio(msgTipo6)
                                        print("erro na quantidade de bytes")
                                else:
                                    msgTipo6=cria_head(6,cont,numPckg,0)
                                    msgTipo6=msgTipo6+eop_fixo 
                                    com1.sendData(np.asarray(msgTipo6))
                                    log_envio(msgTipo6)
                                    print("erro número do pacote")
                            else:
                                msgTipo6=cria_head(6,cont,numPckg,0)
                                msgTipo6=msgTipo6+eop_fixo 
                                com1.sendData(np.asarray(msgTipo6))
                                log_envio(msgTipo6)
                                print("erro número do pacote")
                        else:
                            time.sleep(1)

                            time_now = int (time.time())
                            if time_now >= timer2 + seconds_to_go_for:
                                print("Timer 2 encerrado. Timeout de envio do arquivo, finalizando a comunicação.")
                                ocioso = True

                                msgTipo5=cria_head(5,cont,numPckg,0)
                                msgTipo5=msgTipo5+eop_fixo 

                                com1.sendData(np.asarray(msgTipo5))
                                log_envio(msgTipo5)
                                encerrar=True

                            else:
                                if head == (255).to_bytes(1, byteorder='big'):
                                    msgTipo4=cria_head(4,cont,numPckg,0)
                                    msgTipo4=msgTipo4+eop_fixo 
                                    com1.sendData(np.asarray(msgTipo4))
                                    log_envio(msgTipo4)
                    else:
                        break
                if encerrar==True:
                    break

        com1.disable()
        with open("C:/Users/thpro/Desktop/Camada Física/projetosCamada/p4Protocolo/server/log.txt", "a") as file:
            file.write("Comunicação encerrada")

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

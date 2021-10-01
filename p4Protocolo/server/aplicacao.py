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
    

def create_eop():
    print("função eop")
    eop = b'\xFF\xAA\xFF\xAA'
    return (eop)

def create_head(tipo, total_package, package_number, payload_len, restart_package, last_package):
    print("função head")
    h0 = (tipo).to_bytes(1,byteorder = 'big')
    print(f'O tipo da mensagem colocado no head é:\n{h0}')
    h1 = (0).to_bytes(1,byteorder = 'big')
    h2 = (0).to_bytes(1,byteorder = 'big') 
    h3 = (total_package).to_bytes(1,byteorder ='big')
    h4 = (package_number).to_bytes(1,byteorder ='big')
    h5 = (payload_len).to_bytes(1,byteorder ='big')
    h6 = (restart_package).to_bytes(1,byteorder ='big')
    h7 = (last_package).to_bytes(1,byteorder ='big')
    h8 = (0).to_bytes(1,byteorder = 'big')
    h9 = (0).to_bytes(1,byteorder = 'big')
   

    head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
    
    if len(head) == 10:
        return (head) #bytes e int 
    else:
        print('head != 10')

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM3')
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("comunicacao aberta")

        ocioso = True

        while ocioso:
            rxBuffer, nRx = com1.getData(10)
            if rxBuffer[0] == 1:
                if rxBuffer[2]:
                    ocioso = False
            time.sleep(1)

        numPckg = rxBuffer[3]

        com1.sendData()
        cont = 1

        while cont <= numPckg:
            recebeu = False
            seconds_to_go_for = 20
            timer2 = int(time.time())

            while not recebeu:
                head = com1.getData(10)
                payload = com1.getData(head[5])
                eop = com1.getData(4)
                if head[0] == 3:
                    recebeu = True
                    if head[4] == head[7] + 1:
                        if len(payload) == head[5]:
                            #lista[cont] = payload
                            tipo4 = create_head(4,head[3],head[4],head[5],head[6],head[7]) + payload + create_eop
                            com1.sendData(tipo4)
                            cont+=1
                        else: 
                            tipo6 = create_head(6,head[3],head[4],head[5],head[6],head[7]) + payload + create_eop
                            com1.sendData(tipo6)
                    else:
                        tipo6 = create_head(6,head[3],head[4],head[5],head[6],head[7]) + payload + create_eop
                        com1.sendData(tipo6)
                else:
                    time.sleep(1)

                    time_now = int (time.time())
                    if time_now >= timer2 + seconds_to_go_for:
                        ocioso = True
                        tipo5 = create_head(5,head[3],head[4],head[5],head[6],head[7]) + payload + create_eop
                        com1.sendData(tipo5)
                        com1.disable()

                    else:
                        if head == (255).to_bytes(1, byteorder='big'):
                            tipo4 = create_head(4,head[3],head[4],head[5],head[6],head[7]) + payload + create_eop
                            com1.sendData(tipo4)




    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

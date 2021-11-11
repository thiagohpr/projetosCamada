

#importe as bibliotecas
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
from suaBibSignal import signalMeu


frequencias={0:[941,1336],1:[697,1209],2:[697,1336],3:[697,1477],4:[770,1209],5:[770,1336],6:[770,1477],7:[852,1209],8:[852,1336],9:[852,1477]}


# def signal_handler(signal, frame):
#         print('You pressed Ctrl+C!')
#         sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
     #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    sinal=signalMeu()

    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs=44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    #tempo em segundos que ira emitir o sinal acustico 
    duration = 4
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    perguntando=True
    while perguntando:
        NUM=input("Digite uma tecla de 0 a 9: ")
        if NUM in str(list(frequencias.keys())):
            perguntando=False
            NUM=int(NUM)
    #nao aceite outro valor de entrada.
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    
    
    #construa o sinal a ser reproduzido. nao se esqueca de que é a soma das senoides
    f1=frequencias[NUM][0]
    f2=frequencias[NUM][1]
    
    x1,s1=sinal.generateSin(f1,gainX,duration,fs)
    x2,s2=sinal.generateSin(f2,gainY,duration,fs)
    
    #printe o grafico no tempo do sinal a ser reproduzido
    plt.plot(x1,s1+s2)
    plt.title(f'Senóide {f1}Hz e {f2}Hz pelo tempo do emissor')
    
    sinal.plotFFT(s1+s2,fs)
    
    # reproduz o som
    sd.play(s1+s2, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()

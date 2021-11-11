#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import time
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
from suaBibSignal import signalMeu
import peakutils
from peakutils.plot import plot as pplot



frequencias={(941,1336):0,(697,1209):1,(697,1336):2,(697,1477):3,(770,1209):4,(770,1336):5,(770,1477):6,(852,1209):7,(852,1336):8,(852,1477):9}


def identificaPicos(indexes):
    frequencias2=[941,1336,697,1209,1477,770,852]
    erro=1
    lista=[]
    for pico in indexes:
        for freq in frequencias2:
            if pico>=freq-erro and pico<=freq+erro:
                lista.append(freq)
    if len(lista)!=2:
        print(len(lista))
        return "Erro"
    else:
        return lista[0],lista[1]

def identificaTecla(f):
    return frequencias[f]

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)
    sinal=signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs=44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    


    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    espera=5
    print(f'A captação começará em {espera} segundos.')
    time.sleep(espera)
   
    #faca um print informando que a gravacao foi inicializada
    print('Início da gravação')
   
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    duration = 5
    numAmostras=duration*fs
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
   
    audio = sd.rec(int(numAmostras), fs, channels=1)
    sd.wait()
    print("...     FIM")
    
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    y=[]
    for v in audio:
        y.append(v[0])

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0,duration,numAmostras)

    # plot do grafico  áudio vs tempo!

    plt.plot(t, y)
    plt.title('Áudio recebido no domínio do Tempo')
   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = sinal.calcFFT(y, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = peakutils.indexes(yf,thres=0.3,min_dist=100)
    pplot(xf, yf, index)
    #printe os picos encontrados! 
    #https://peakutils.readthedocs.io/en/latest/reference.html
    #https://peakutils.readthedocs.io/en/latest/tutorial_a.html
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    # print(f'Frequência 1:{xf[index[0]]}')
    # print(f'Frequência 2:{xf[index[1]]}')
    freq=[]
    for i in index:
        freq.append(xf[i])
    print("Apertou a tecla: {}".format(identificaTecla(identificaPicos(freq))))
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()

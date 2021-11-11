#importe as bibliotecas
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
from suaBibSignal import signalMeu
from funcoes_LPF import LPF

def main():
    sinal=signalMeu()
    print("Inicializando encoder")
    figure,axs = plt.subplots(2, 3)
    # 1. Faça a leitura de um arquivo de áudio .wav de poucos segundos (entre 2 e 5) previamente gravado com uma
    # taxa de amostragem de 44100Hz.
    data, fs = sf.read('my-file2.wav')

    # 2. Normalize esse sinal: multiplicar o sinal por uma constante (a maior possível), de modo que todos os pontos
    # do sinal permaneçam dentro do intervalo[-1,1].
    time=5
    n = time*fs
    x = np.linspace(0.0, time, n)
    k=1/max(abs(data))
    print(f'Plotando o sinal com k={k}')
    axs[0,0].set_title(f'Gráfico 1: Sinal k*data, com k={k}')
    axs[0,0].plot(x,k*data)

    k_data=k*data

    # 3. Filtre e elimine as frequências acima de 4kHz.
    print('Filtrando o sinal com Low Pass Filter')
    low_pass_freq=4000
    k_data_lpf=LPF(k_data,low_pass_freq,fs)

    print(f'Plotando o sinal com k={k}')
    axs[0,1].set_title(f'Gráfico 2: Sinal filtrado no tempo')
    axs[0,1].plot(x,k_data_lpf)

    xf, yf = sinal.calcFFT(k_data_lpf, fs)
    axs[0,2].set_title('Gráfico 3: Sinal filtrado na frequência')
    axs[0,2].plot(xf,yf)

    # 4. Reproduza o sinal e verifique que continua audível (com menos qualidade).
    sd.play(k_data_lpf, fs)
    sd.wait()

    # 5. Module esse sinal de áudio em AM com portadora de 14 kHz. (Essa portadora deve ser uma senoide
    # começando em zero)
    x2,portadora=sinal.generateSin(14000,1,5,fs)

    sinal_modulado=(k_data_lpf)*portadora
    axs[1,0].set_title(f'Gráfico 4: Sinal modulado no tempo')
    axs[1,0].plot(x,sinal_modulado)
    
    xf2, yf2 = sinal.calcFFT(sinal_modulado, fs)
    axs[1,1].set_title('Gráfico 5: Sinal modulado na frequência')
    axs[1,1].plot(xf2,yf2)
    
    # 6. Execute e verifique que não é perfeitamente audível.

    #Está comentado pois o áudio dói o ouvido.
    # sd.play(sinal_modulado, fs)
    # sd.wait()

    # 7. Envie um arquivo com áudio modulado para sua dupla ou, mais divertido, execute o áudio e peça para que
    # seu colega grave o áudio modulado.
    sf.write('modulado.wav', sinal_modulado, fs)
    print('Arquivo de áudio modulado salvo!')
    plt.show()

if __name__ == "__main__":
    main()

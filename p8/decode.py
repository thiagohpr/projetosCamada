#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window
from suaBibSignal import signalMeu
from peakutils.plot import plot as pplot
from funcoes_LPF import LPF


def main():
    figure,axs = plt.subplots(1,2)
    print("Inicializando decoder")

    # 8. Verifique que o sinal recebido tem a banda dentro de 10kHz e 18kHz (faça o Fourier).
    sinal=signalMeu()
    modulado, fs = sf.read('modulado.wav')

    # 9. Demodule o áudio enviado pelo seu colega.
    print('Demodulando o sinal')
    x2,portadora=sinal.generateSin(14000,1,5,fs)
    demodulado=modulado*portadora

    xf, yf = sinal.calcFFT(demodulado, fs)
    axs[0].set_title('Gráfico 6: Sinal demodulado no domínio da frequência')
    axs[0].plot(xf,yf)
    
    # 10. Filtre as frequências superiores a 4kHz.
    print('Filtrando o sinal com Low Pass Filter')
    low_pass_freq=4000
    demodulado_lpf=LPF(demodulado,low_pass_freq,fs)

    xf2, yf2 = sinal.calcFFT(demodulado_lpf, fs)
    axs[1].set_title('Gráfico 7: Sinal demodulado e filtrado no domínio da frequência')
    axs[1].plot(xf2,yf2)
    
    plt.show()
    # 11. Execute o áudio do sinal demodulado e verifique que novamente é audível.
    print('Executando o áudio demodulado')
    sd.play(demodulado_lpf, fs)
    sd.wait()

if __name__ == "__main__":
    main()

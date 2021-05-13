# %%
from suaBibSignal import *
from funcoes_LPF import *
import peakutils  # alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import time


def checkBand(x, y):
    j = 0
    for i in range(0, 16000):
        if y[i] < 10:
            j += 1

    if j > 15900 and np.max(x) < 24000:
        return 'SINAL MODULADO DENTRO DA BANDA DE 16KHz e 24KHz'
    else:
        return 'SINAL MODULADO COM ERROS'


def plot(title, signal, xlim_signal, xlim_fourier, fs):
    s = signalMeu()
    plt.figure()
    plt.plot(signal)
    plt.title("Sinal {}".format(title))
    plt.xlim(0, xlim_signal)
    plt.show()

    plt.figure()
    X, Y = s.calcFFT(signal, fs)
    plt.plot(X, np.abs(Y))
    plt.xlim(0, xlim_fourier)
    plt.ylim(0, 500)
    plt.title("{} -- Fourier".format(title))
    plt.show()

    return X, Y


def main():
    s = signalMeu()
    filename = 'myhump.wav'
    dataPre, fs = sf.read(filename, dtype='float32')
    amin, amax = np.min(dataPre), np.max(dataPre)

    print("Normalizando audio...")

    data = []
    for i, val in enumerate(dataPre):
        avg = (amin+amax)/2
        ran = (amax-amin)/2
        data.append((val-avg)/ran)

    print('Normalizacao completa')

    filtered = LPF(data, 4000, fs)

    carrier_freq = 20000
    Te = 1
    t = np.linspace(-1, 1, 1*fs*3)

    x_car, y_car = s.generateSin(carrier_freq, 1, 3, fs)
    carrier = y_car

    modulated = filtered*carrier
    print(modulated)
    plot(title='arquivo original', signal=dataPre,
         xlim_signal=14000, xlim_fourier=9000, fs=fs)
    plot(title='normalizado', signal=data,
         xlim_signal=150000, xlim_fourier=9000, fs=fs)
    plot(title='filtrado', signal=filtered,
         xlim_signal=200000, xlim_fourier=9000, fs=fs)
    x_fou_mod, y_fou_mod = plot(
        title="modulado", signal=modulated, xlim_signal=240000, xlim_fourier=20000, fs=fs)



    # DEMODULACAO
    print("--------------------------------")
    
    print(checkBand(x_fou_mod, y_fou_mod))

    print("\n")
    print("SINAL MODULADO COM SUCESSO\n")
    print("INICIANDO DEMODULACAO DE SINAL\n")
    print("\n")

    # ler arquivo modulado enviado por colega e verificar banda
    # audioLido,fs = sf.read(filename, dtype='float32')
    # x,y = plot(title="audio modulado lido", signal=audioLido, xlim_signal=24000, xlim_fourier=24000, fs=fs)
    # print(checkBand(x,y))
    # demodulated = audioLido*carrier

    demodulated = modulated*carrier

    print("DEMODULACAO COMPLETA, INICIANDO FILTRO DE FREQUENCIAS")

    x_demod, y_demod = plot(title="Demodulado", signal=demodulated,
                            xlim_signal=24000, xlim_fourier=10000, fs=fs)

    print(np.max(modulated))
    demod_filter = filtro(demodulated, 3000, fs)

    print("AUDIO DEMODULADO E FILTRADO")
    print("--------------------------------")

    sd.play(demod_filter)
    sd.wait()


    


if __name__ == '__main__':
    main()
# %%

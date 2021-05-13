import sys
sys.path.append('')
import numpy as np
from suaBibSignal import *
import sounddevice as sd
import time
from scipy.io.wavfile import write


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
  s = signalMeu()
  fs = 44100
  duration = 3
  numAmostras = duration * fs

    
  sd.default.samplerate = fs  
  sd.default.channels = 1 

  print('A GRAVACAO SERA INICIADA EM 5 SEGUNDOS')
  time.sleep(5)
  print('GRAVACAO INICADA') 

  audio = sd.rec(int(numAmostras), dtype='float32')
  sd.wait()

  print("FIM DA GRAVACAO")
  write('myhump.wav', fs, audio)


if __name__ == "__main__":
    main()
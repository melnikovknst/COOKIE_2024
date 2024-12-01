'''draws files from input_dir which are .npy
   for proper work files must be in format channel1| ... | channel4 (without any splitters in between)
   input - string (filename)
   input - int (n files to read from input_dir)
'''
import os

import numpy as np
import matplotlib.pyplot as plt

from scipy import signal
from scipy.fftpack import fft, ifft


def draw_spectogram(file:str, step:int = 1000):
    arr = np.fromfile(file, dtype=np.float32)
    if (arr.shape[0] != 128000 * 4):
        arr = np.fromfile(file, dtype=np.int16)
    arr = np.array(np.split(arr, 4))
    print(len(arr[0, :]))

    hopsamp = step // 2
    lx = np.zeros(hopsamp)
    rx = np.zeros(hopsamp * 2)
    arr = np.hstack((lx, arr[0, :], rx))

    w = np.hanning(step + 1)[:-1]
    res = np.array([np.fft.fftshift(fft(np.fft.ifftshift(w * arr[i:i+step])))/hopsamp for i in range(0, len(arr)-step, hopsamp)])

    plt.imshow(np.abs(res), aspect='auto')



def main() -> None:
    input_dir:str = r".\input"
    files_to_draw = input()

    try:
        files_to_draw = int(files_to_draw)
        for i in range(files_to_draw):
            draw_spectogram(os.path.join(input_dir, os.listdir(input_dir)[i]))
    except ValueError:
        try:
            if not files_to_draw.endswith(".npy"):
                print("File is not a numPy file.\nExiting...")
            else:
                draw_spectogram(os.path.join(input_dir, files_to_draw))
        except FileNotFoundError:
            print("file", files_to_draw, "doesn't exist.\nExiting...")

    plt.show()

if __name__ == "__main__":
    main()
'''converts all files from input_dir which are .npy
   for proper work files must be in format channel1| ... | channel4 (without any splitters in between)
'''
import os

import numpy as np
import matplotlib.pyplot as plt

def create_sub_plots(file:str):
    arr = np.fromfile(file, dtype=np.float32)
    if (arr.shape[0] != 128000*4):
        arr = np.fromfile(file, dtype=np.int16)
    arr = np.array(np.split(arr, 4))

    time = np.linspace(0, arr.shape[1]/128000, arr.shape[1])

    sb, ax = plt.subplots(nrows=2, ncols=2)
    ax[0][0].plot(time, arr[0])
    ax[0][1].plot(time, arr[1])
    ax[1][0].plot(time, arr[2])
    ax[1][1].plot(time, arr[3])


def main() -> None:
    input_dir:str = r".\input"
    files_to_draw = input()

    try:
        int(files_to_draw)
        for i in range(files_to_draw):
            create_sub_plots(os.path.join(input_dir, os.listdir(input_dir)[i]))
    except ValueError:
        try:
            if not files_to_draw.endswith(".npy"):
                print("File is not a numPy file.")
            else:
                create_sub_plots(os.path.join(input_dir, files_to_draw))
        except FileNotFoundError:
            print("file", files_to_draw, "doesn't exist.\nExiting...")

    plt.show()

if __name__ == "__main__":
    main()



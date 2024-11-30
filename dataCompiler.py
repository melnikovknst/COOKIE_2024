import os
import numpy as np
import filter
from scipy import signal


def process(file, input_dir=".\\input\\", output_dir=".\\output\\") -> None:
    samplerate = 128000

    arr = np.fromfile(input_dir + file, dtype=np.int16) #reading splitted files

    arr = np.array(np.array_split(arr, 4), dtype=np.float64).T #spliting into 4 channels, and transposing for filtration

    #detrend
    for i in range(0, arr.shape[0]):
        arr[i] = signal.detrend(arr[i], type="linear")

    #filter
    cls = filter.BandPassFiltration()
    filter_data = lambda trace: cls.filter_data(trace, freq_sample_rate=samplerate, frequency=[5, 2000], order=1)
    filtered_data = np.array([filter_data(arr[:, i]) for i in range(arr.shape[1])]).T

    #normalization
    for i in range(0, filtered_data.shape[1]):
        filtered_data[:, i] /= np.max(filtered_data[:, i])

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    try:
        os.remove(output_dir + file)
    except FileNotFoundError:
        pass
    with open(output_dir + file, "wb") as f:
        for i in range(filtered_data.shape[1]):
            f.write(arr[:, i])


def main():
    dir = '.\\input\\'
    files = []
    for i in os.listdir(dir):
        if i.endswith(".npy"):
            files.append(i)

    for file in files:
        process(file)


if __name__ == "__main__":
    main()
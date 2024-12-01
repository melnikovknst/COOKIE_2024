import os
import numpy as np
import filter
from scipy import signal
from matplotlib import pyplot as plt


def process(file, input_dir=".\\input\\", output_dir=".\\output\\") -> None:
    samplerate = 128000

    arr = np.fromfile(input_dir + file, dtype=np.int16) #reading splitted files

    arr = np.array(np.array_split(arr, 4), dtype=np.float32).T #spliting into 4 channels, and transposing for filtration

    cls = filter.BandPassFiltration()
    detrend_trace = lambda trace: signal.detrend(trace)
    filter_trace = lambda trace: cls.filter_data(trace, freq_sample_rate=samplerate, frequency=[5, 15000], order=1)
    norm_data = lambda data: data / np.max(abs(data))

    arr_prepared = np.zeros_like(arr)
    for i in range(arr.shape[1]):
        trace = arr[:, i]
        detrended_trace = detrend_trace(trace)
        filtered_trace = filter_trace(detrended_trace)
        arr_prepared[:, i] = filtered_trace
    arr_norm = norm_data(arr_prepared)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    try:
        os.remove(output_dir + file)
    except FileNotFoundError:
        pass
    with open(output_dir + file, "wb") as f:
        for i in range(arr_norm.shape[1]):
            f.write(arr_norm[:, i])


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
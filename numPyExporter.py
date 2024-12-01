import os.path

from scipy.io import wavfile
import numpy as np


def slicefile(input_dir:str, file:str, channels:int) -> np.ndarray:
    samplerate, data = wavfile.read(os.path.join(input_dir, file))
    tmp = []
    unsorted_res = []

    length = data.shape[0] / samplerate

    for channel in range(channels):
        tmp = [data[i][channel] for i in range(0, data.shape[0])]
        for i in range(0, int(length)):
            unsorted_res.append([tmp[j] for j in range(samplerate * i, samplerate * (i+1))])

    res = []
    tmp = []

    for second in range(int(length)):
        for i in range(second, len(unsorted_res), len(unsorted_res)//channels):
            tmp.append(unsorted_res[i])
        res.append(tmp)
        tmp = []

    res = np.array(res, dtype=np.int16)

    return res


def dump(path:str, filename:str, arr:list) -> None:
    if not os.path.exists(path):
        os.mkdir(path)

    #try:
    #    os.remove(os.path.join(path, filename))
    #except FileNotFoundError:
    #    pass

    with open(os.path.join(path, filename), "wb") as file:
        for i in range(len(arr)):
            file.write(arr[i])


def get_date_from_filename(filename:str) -> list:
    tmp = filename.split("_")
    for i in range(len(tmp)):
        if tmp[i] == "to":
            return [[tmp[i - 7], tmp[i - 6], tmp[i - 5], tmp[i - 3], tmp[i - 2], tmp[i - 1]], [tmp[i + 1], tmp[i + 2], tmp[i + 3], tmp[i + 5], tmp[i + 6], tmp[i + 7][0:2]]]


def format_date(date:list, second:int) -> str:
    seconds = int(date[0][5])
    minutes = int(date[0][4])
    hours = int(date[0][3])

    seconds += second

    while (seconds > 60):
        minutes += 1
        seconds %= 60
    while (minutes > 60):
        hours += 1
        minutes %= 60

    hours = str(hours)
    minutes = str(minutes)
    seconds = str(seconds)

    if len(hours) == 1:
        hours = '0' + str(hours)
    if len(minutes) == 1:
        minutes = ('0' + str(minutes))
    if len(seconds) == 1:
        seconds = ('0' + str(seconds))

    return date[0][0] + '-' + date[0][1] + '-' + date[0][2] + ' ' + hours + '-' + minutes + '-' + seconds + '.npy'

def main() -> None:
    output_dir = r".\output"
    input_dir = r".\data\2024_06_01"

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for i in os.listdir(input_dir):
        if i.endswith(".wav"):
            arr = slicefile(input_dir, i, 4)
            print("parsing file: ", i)

            for j in range(len(arr)):
                dump(output_dir, format_date(get_date_from_filename(i), j), arr[j])


def sliceAndDump(input_path:str, output_path:str) -> None:
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for i in os.listdir(input_path):
        if i.endswith(".wav"):
            arr = slicefile(r"C:\Users\Alex\Documents\COOCKIE_2024\data\2024_06_01\d001_msi_fragment_2024_06_01__14_33_20_to_2024_06_01__14_34_50.wav", 4)
            print("parsing file: ", i)

            for j in range(len(arr)):
                dump(output_path, format_date(get_date_from_filename(i), j), arr[j])

if __name__ == "__main__":
    main()
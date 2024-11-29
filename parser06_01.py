import os
import wave

data_path = r".\data\2024_06_01"

files = []
buff = ''
channels:int = 0
frequency:int = 0


def little_endian_to_int(str) -> int:
    return int.from_bytes(str, "little", signed=True)

for i in os.listdir(data_path):
    files.append(os.path.join(data_path, i))

for filenum in range(0, len(files)):
    with wave.open(files[filenum], "rb") as file:
        n = 0
        res1 = []
        res2 = []
        res3 = []
        res4 = []
        for n in range(0, int(file.getnframes() / 128)):
            res1.append(0)
            res2.append(0)
            res3.append(0)
            res4.append(0)
            for i in range(0, 128):
                buff = file.readframes(1)
                res1[n] += little_endian_to_int(buff[0:2])
                res2[n] += little_endian_to_int(buff[2:4])
                res3[n] += little_endian_to_int(buff[4:6])
                res4[n] += little_endian_to_int(buff[6:8])

            res1[n] /= 128
            res2[n] /= 128
            res3[n] /= 128
            res4[n] /= 128

    with open(files[filenum] + ".csv", "x") as out:
        out.write("time; sensor1; sensor2; sensor3; sensor4\n")
        for i in range(0, len(res1)):
            out.write(str(i) + ";" + str(res1[i]) + ";" + str(res2[i]) + ";" + str(res3[i]) + ";" + str(res4[i]) + "\n")
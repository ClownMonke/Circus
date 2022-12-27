from Freq_extension import FreqList
from Log_files import LogFile
from random import random

log_file_name = 'delete.txt'

freq_list = [1e3, 1e4, 5e4, 1e5]  # Freq List

c_d_r_x = [0, 0, 0, 0]

log_file = LogFile(log_file_name)
time = 1
current_freq = FreqList(freq_list)
for i in range(100):
    time = time * 1.12
    temperature = random()*200
    freq = current_freq.get_next_freq()
    c_d_r_x[0] = random()*1e-10
    c_d_r_x[1] = random()*0.3
    c_d_r_x[2] = random()*20e3
    c_d_r_x[3] = random()*200e3

    log_file.print(time, temperature, freq, c_d_r_x)


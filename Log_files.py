from typing import IO


class LogFile:
    __log_file: IO

    def __init__(self, log_file_name):
        self.__log_file = open(log_file_name, 'w')
        self.__log_file.write('Time_s\tTemp_C\tFreq_Hz\tC_F\tD_1\tR_Ohm\tX_Ohm\n')

    def __del__(self):
        print("Log file CLOSED")
        self.__log_file.close()

    def print(self, time, temperature, frequency, c_d_r_x):
        msg = ("{:7.0f}".format(time) + '\t' +
               "{:5.1f}".format(temperature) + '\t' +
               "{:9.2f}".format(frequency) + '\t' +
               "{:+.5e}".format(c_d_r_x[0]) + '\t' +
               "{:+.5e}".format(c_d_r_x[1]) + '\t' +
               "{:+.5e}".format(c_d_r_x[2]) + '\t' +
               "{:+.5e}".format(c_d_r_x[3]) + '\n')
        print(msg)
        self.__log_file.write(msg)





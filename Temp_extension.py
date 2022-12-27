import serial
import numpy as np
import time


class TempController:
    __serial_obj:  serial.Serial
    __temperature: float

    def __init__(self, com_port_name):
        self.__serial_obj = serial.Serial(com_port_name, baudrate=115200, timeout=30)
        self.__get_init_temp()
        print('COM port connected')

    def __del__(self):
        if hasattr(self, '__serial_obj'):
            self.__serial_obj.close()
            print('COM port to thermocontroller CLOSED')
        else:
            print('thermocontroller COM port: nothing to close')

    def set_temp_rate(self, temp_target=25, temp_rate=360/3):
        temp_rate = np.uint16(temp_rate)
        t_tar = np.uint16(temp_target * 100)
        t_tar_low = np.uint8(t_tar & 255)
        t_tar_high = np.uint8(t_tar >> 8)
        rate_low = np.uint8(temp_rate & 255)
        rate_high = np.uint8(temp_rate >> 8)
        self.__serial_obj.flushOutput()
        control_data = ([6, 1, rate_high, rate_low, t_tar_high, t_tar_low])
        self.__serial_obj.write(control_data)

    def get_temp(self):
        bytes_count = self.__serial_obj.in_waiting
        if bytes_count >= 44:
            ser_bytes = self.__serial_obj.read(44)
            self.__temperature = ((ser_bytes[4] << 8) + (ser_bytes[5])) / 100
            self.__serial_obj.flushInput()
        return self.__temperature

    # -----------------------------------PRIVATE PART---------------------------------------
    def __get_init_temp(self):
        self.__serial_obj.flushInput()
        bytes_count = self.__serial_obj.in_waiting
        while bytes_count < 1:
            bytes_count = self.__serial_obj.in_waiting
        time.sleep(0.2)
        self.__serial_obj.flushInput()
        ser_bytes = self.__serial_obj.read(44)
        self.__serial_obj.flushInput()
        self.__temperature = ((ser_bytes[4] << 8) + (ser_bytes[5])) / 100




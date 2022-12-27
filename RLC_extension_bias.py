import pyvisa as visa
import time


class LCRmeter:
    __cmd_wait_time = 0.1
    __resource_manager = visa.ResourceManager()
    __device: __resource_manager.open_resource

    def __init__(self):
        self.__device = self.__connect()
        self.set_voltage(0.01)
        self.set_frequency(1000)

    def __del__(self):
        self.__disconnect()

    # TODO: leave only 2 methods to set
    def set_voltage(self, volt=0.01):
        self.__device.write(':VOLTage:LEVel ' + str(volt))
        time.sleep(self.__cmd_wait_time)

    def set_get_voltage(self, volt=0.01):
        self.set_voltage(volt)
        out_volt = self.__device.query(':VOLTage:LEVel?')
        return out_volt

    def set_frequency(self, freq=1000):
        self.__device.write(':FREQuency:CW ' + str(freq))
        time.sleep(self.__cmd_wait_time)

    def set_get_frequency(self, freq=1000):
        self.set_frequency(freq)
        out_freq = self.__device.query(':FREQuency:CW?')
        return out_freq

    def get_c_d_r_x(self) -> list[float]:
        z = self.__device.query(':FETCh:IMPedance:FORmatted?')
        values_arr_c_d = z.split(',', 2)
        z = self.__device.query(':FETCh:IMPedance:CORrected?')
        values_arr_r_x = z.split(',', 2)
        c_d_r_x = [float(values_arr_c_d[0]),
                   float(values_arr_c_d[1]),
                   float(values_arr_r_x[0]),
                   float(values_arr_r_x[1])]
        return c_d_r_x

    def set_bias_state_amp(self, bias_state=0, bias_amp=0):
        self.__device.write(':BIAS:STATe ' + str(bias_state))
        time.sleep(self.__cmd_wait_time)
        self.__device.write(':BIAS:VOLTage:LEVel ' + str(bias_amp))
        time.sleep(self.__cmd_wait_time)
        # state = self.__device.query(':BIAS:STATe?')
        # ampl = self.__device.query(':BIAS:VOLTage:LEVel?')
        # print('BIAS voltage is ' + str(ampl))

    # -----------------------------------PRIVATE PART---------------------------------------
    def __find_rlc(self):
        rm_list = self.__resource_manager.list_resources()
        for adr in rm_list:
            # print(name)
            try:
                instrument = self.__resource_manager.open_resource(adr)
                idn = instrument.query('*IDN?')
                instrument.close()
                if idn == "Keysight Technologies,E4980AL,MY54305367,B.07.01\n":
                    return adr
            except:
                pass
        return 0

    def __connect(self):
        rlc_adr = self.__find_rlc()
        if rlc_adr != 0:
            device = self.__resource_manager.open_resource(rlc_adr)
            idn = device.query('*IDN?')
            print('RLC device connected:\n' + idn + '\n')
            return device
        else:
            print('\nno RLC device found\n')
            exit(-1)


    def __disconnect(self):
        self.__device.close()
        print('RLC device CLOSED')








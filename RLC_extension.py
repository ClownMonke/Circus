import pyvisa as visa

resource_manager = visa.ResourceManager()


def _find_rlc():
    rm_list = resource_manager.list_resources()
    for name in rm_list:
        # print(name)
        try:
            Instrument = resource_manager.open_resource(name)
            idn = Instrument.query('*IDN?')
            Instrument.close()
            if idn == "Keysight Technologies,E4980AL,MY54305367,B.07.01\n":
                return name
        except:
            pass
    return 0


def connect():
    rlc_adr = _find_rlc()
    if rlc_adr != 0:
        device = resource_manager.open_resource(rlc_adr)
        idn = device.query('*IDN?')
        print('RLC device ready:\n' + idn + '\n')
    else:
        device = 0
        print('\nno RLC device found\n')
        exit(-1)
    return device


def disconnect(device):
    device.close()
    print('RLC device closed')


def get_data(device):
    z = device.query(':FETCh:IMPedance:FORmatted?')
    values_arr_c_d = z.split(',', 2)
    value = (values_arr_c_d[0])  # for plotting
    z = device.query(':FETCh:IMPedance:CORrected?')
    values_arr_r_x = z.split(',', 2)
    c_d_r_x = [values_arr_c_d[0], values_arr_c_d[1], values_arr_r_x[0], values_arr_r_x[1]]
    return c_d_r_x


def set_frequency(device, volt, freq, delimiter=','):
    if delimiter == ',':
        print(':VOLTage:LEVel ' + str(volt).replace('.', ','))
        device.write(':VOLTage:LEVel ' + str(volt).replace('.', ','))
        device.write(':FREQuency:CW ' + str(freq).replace('.', ','))
    elif delimiter == '.':
        device.write(':VOLTage:LEVel ' + str(volt))
        device.write(':FREQuency:CW ' + str(freq))


def set_amp(device, volt):
    null = device.write(':VOLTage:LEVel ' + str(volt))


# def set_frequency(volt, freq, delimiter=','):
#     if delimiter == ',':
#         print(':VOLTage: LEVel ' + str(volt).replace('.', ','))
#         print(':FREQuency: CW ' + str(freq).replace('.', ','))
#     elif delimiter == '.':
#         print(':VOLTage: LEVel ' + str(volt))
#         print(':FREQuency: CW ' + str(freq))

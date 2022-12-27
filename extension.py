import pyvisa as visa

rm = visa.ResourceManager()
Rm_list = rm.list_resources()


def find_rlc():
    for name in Rm_list:
        # print(name)
        try:
            Instrument = rm.open_resource(name)
            idn = Instrument.query('*IDN?')
            Instrument.close()
            if idn == "Keysight Technologies,E4980AL,MY54305367,B.07.01\n":
                return name
        except:
            pass
    return 0





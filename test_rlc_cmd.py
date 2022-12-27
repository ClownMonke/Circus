from RLC_extension_bias import LCRmeter

freq = 1231
volt = 0.02
bias_state = 0
bias_amplitude = 0

lcr_device = LCRmeter()
lcr_device.set_frequency(freq)
lcr_device.set_voltage(volt)
lcr_device.set_bias_state_amp(bias_state, bias_amplitude)


# import RLC_extension

# device = RLC_extension.connect()

# RLC_extension.set_frequency(device, 0.3, 1050, '.')

# data = RLC_extension.get_data(device)
# print(data)
# print('start')
# RLC_extension.set_frequency(device, 0.2, 1123,'.')
# print('ok')

# RLC_extension.disconnect(device)






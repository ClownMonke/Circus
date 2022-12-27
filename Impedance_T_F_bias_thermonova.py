import time
import keyboard
import draw_lib
from RLC_extension_bias import LCRmeter
from Temp_extension import TempController
from Log_files import LogFile
from Freq_extension import FreqList

# ===========================================
T_target1 = 425  # [C] (Первая целевая температура)
T_target2 = 30  # [C] (Вторая целевая температура)
rate = 100  # [C/hour] (скорость)
measurement_frequency = 1000  # [Hz]
measurement_voltage = 0.05  # [V]
freq_list = [20.0000000000000,
28,
39.2000000000000,
54.8800000000000,
76.8320000000000,
107.564800000000,
150.590720000000,
210.827008000000,
295.157811200000,
413.220935680000,
578.509309952000,
809.913033932799,
1133.87824750592,
1587.42954650829,
2222.40136511160,
3111.36191115624,
4355.90667561874,
6098.26934586623,
8537.57708421272,
11952.6079178978,
16733.6510850569,
23427.1115190797,
32797.9561267116,
45917.1385773962,
64283.9940083547,
89997.5916116966,
125996.628256375,
176395.279558925,
246953.391382495,
300000]  # Freq List
bias_state = 0  # 0 - OFF, 1 - ON
bias_amp = 0  # [V]
com_port_name = 'COM3'
log_file_name = 'log 2022_12_XX_test.txt'
# ===========================================
delta_limit = T_target1 / 90

# connect to LCR
lcr_device = LCRmeter()
lcr_device.set_frequency(measurement_frequency)
lcr_device.set_voltage(measurement_voltage)
# lcr_device.set_bias_state_amp(bias_state, bias_amp)

# connect to thermocontroller
temp_device = TempController(com_port_name)
temp_device.set_temp_rate(T_target1, rate)

# log file creation
log_file_obj = LogFile(log_file_name)

# Main cycle start
current_freq = FreqList(freq_list)
flag_temp_phase = 0  # 0 - heat, 1 - cool, 2 - cool ended
time_start = time.time()
while flag_temp_phase != 2:
    if keyboard.is_pressed('q'):  # close by q key
        print('You Pressed q Key!')
        break

    # update all variables
    time_pass = time.time() - time_start
    temperature = temp_device.get_temp()
    c_d_r_x = lcr_device.get_c_d_r_x()
    frequency = current_freq.get_next_freq()
    lcr_device.set_frequency(frequency)

    # check temperature phases
    if temperature < T_target1 and flag_temp_phase == 0:
        temp_device.set_temp_rate(T_target1, rate)
        delta = abs(T_target1 - temperature)
        if delta < delta_limit:
            flag_temp_phase = 1

    if flag_temp_phase == 1:
        temp_device.set_temp_rate(T_target2, rate)
        delta = abs(T_target2 - temperature)
        if delta < delta_limit:
            flag_temp_phase = 2

    # draw to window and print to log file
    draw_lib.draw_figure(time_pass, temperature, c_d_r_x)
    log_file_obj.print(time_pass, temperature, frequency, c_d_r_x)

# lcr_device.set_bias_state_amp(0, 0)  # Turning bias off, just in case

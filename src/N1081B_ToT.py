# to run this demo connect OUT-B-0 to IN-A-0 with a lemo cable

import pprint
import time
import matplotlib.pyplot as plt
from N1081B_sdk import N1081B

pp = pprint.PrettyPrinter(indent=4)

# create N1081B board object
N1081B_device = N1081B("192.168.50.153")
# connect to the board
N1081B_device.connect()

# get board information and print them
version_json = N1081B_device.get_version()
pp.pprint(version_json)
serial_number = version_json["data"]["serial_number"]
software_version = version_json["data"]["software_version"]
zynq_version = version_json["data"]["zynq_version"]
fpga_version = version_json["data"]["fpga_version"]

# set input of section A in NIM standard
N1081B_device.set_input_configuration(N1081B.Section.SEC_A,
                                      N1081B.SignalStandard.STANDARD_NIM,
                                      N1081B.SignalStandard.STANDARD_NIM,
                                      0, N1081B.SignalImpedance.IMPEDANCE_50)

# set output of section B in NIM standard
N1081B_device.set_output_configuration(N1081B.Section.SEC_B,
                                       N1081B.SignalStandard.STANDARD_NIM)

# set section A function as time over threshold
N1081B_device.set_section_function(N1081B.Section.SEC_A,
                                   N1081B.FunctionType.FN_TIME_OVER_THRESHOLD)

# set section B function as pulse generator
N1081B_device.set_section_function(N1081B.Section.SEC_B,
                                   N1081B.FunctionType.FN_PULSE_GENERATOR)

# configure the time over threshold (10 ns in the minimum windows size)
N1081B_device.configure_time_over_threshold(N1081B.Section.SEC_A,
                                           True, False, False, False,
                                           10,
                                           512)


# configure the pulse generator (Poisson random generator, width:200ns, period: 10000ns, output all enabled)
N1081B_device.configure_pulse_generator(N1081B.Section.SEC_B,
                                        N1081B.StatisticMode.STAT_POISSON,
                                        2000, 1000000, True, True, True, True)

# reset acquisition on section A
N1081B_device.reset_channel(N1081B.Section.SEC_A,
                            0,
                            N1081B.FunctionType.FN_TIME_OVER_THRESHOLD)

# start acquisition on section A
N1081B_device.start_acquisition(N1081B.Section.SEC_A,
                                N1081B.FunctionType.FN_TIME_OVER_THRESHOLD)

# loop reading the counter values
plt.ion()
plt.show()

while 1:
    # use the generic function get_function_results to get the section A result
    data = N1081B_device.get_function_results(N1081B.Section.SEC_A)

    # decode the counter value of channel 0 (section A)
    value = data["data"]["spectrum1"]
    plt.cla()
    plt.plot(value)
    plt.draw()
    plt.pause(1)


# close connection
N1081B_device.disconnect()

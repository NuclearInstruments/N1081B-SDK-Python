# to run this demo connect OUT-B-0 to IN-A-0 and OUT-B-1 to IN-A-1 with a lemo cable

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


# set input of section A in NIM standard
N1081B_device.set_input_configuration(N1081B.Section.SEC_A,
                                      N1081B.SignalStandard.STANDARD_NIM,
                                      N1081B.SignalStandard.STANDARD_NIM,
                                      0, N1081B.SignalImpedance.IMPEDANCE_50)

# set output of section B in NIM standard
N1081B_device.set_output_configuration(N1081B.Section.SEC_B,
                                       N1081B.SignalStandard.STANDARD_NIM)

# set section A function as rate meter advanced
N1081B_device.set_section_function(N1081B.Section.SEC_A,
                                   N1081B.FunctionType.FN_AND)

# set section B function as pulse generator
N1081B_device.set_section_function(N1081B.Section.SEC_B,
                                   N1081B.FunctionType.FN_PULSE_GENERATOR)

# configure the the AND function enabling only channel 0 and 1; disable bypass
N1081B_device.configure_and(N1081B.Section.SEC_A,
                            True, True, False, False, False, False,
                            False,
                            0)

# configure the pulse generator (Poisson random generator, width:200ns, period: 10000ns, output all enabled)
N1081B_device.configure_pulse_generator(N1081B.Section.SEC_B,
                                        N1081B.StatisticMode.STAT_POISSON,
                                        200, 10000, True, True, True, True)




# close connection
N1081B_device.disconnect()

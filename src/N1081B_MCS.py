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
response_json = N1081B_device.set_input_configuration(N1081B.Section.SEC_A,
                                                      N1081B.SignalStandard.STANDARD_NIM,
                                                      N1081B.SignalStandard.STANDARD_NIM,
                                                      0, N1081B.SignalImpedance.IMPEDANCE_50)
pp.pprint(response_json)

# set output of section B in NIM standard
response_json = N1081B_device.set_output_configuration(N1081B.Section.SEC_B,
                                                       N1081B.SignalStandard.STANDARD_NIM)
pp.pprint(response_json)

# check input configuration
pp.pprint(N1081B_device.get_input_configuration(N1081B.Section.SEC_A))

# set section A function as counter
response_json = N1081B_device.set_section_function(N1081B.Section.SEC_A,
                                                   N1081B.FunctionType.FN_COUNTER)
pp.pprint(response_json)

# set section B function as pulse generator
response_json = N1081B_device.set_section_function(N1081B.Section.SEC_B,
                                                   N1081B.FunctionType.FN_PULSE_GENERATOR)
pp.pprint(response_json)

# configure the pulse generator (width:200ns, period: 10000ns, output all enabled)
response_json = N1081B_device.configure_pulse_generator(N1081B.Section.SEC_B,
                                                        N1081B.StatisticMode.STAT_DETERMINISTIC,
                                                        200, 10000, True, True, True, True)
pp.pprint(response_json)

# loop reading the counter values
old_value = 0
while 1:
    # use the generic function get_function_results to get the section A result
    counter_json = N1081B_device.get_function_results(N1081B.Section.SEC_A)

    # decode the counter value of channel 0 (section A)
    value = counter_json["data"]["counters"][0]["value"]
    print(str(value) + "    delta: " + str(value-old_value)) 
    old_value = value
    time.sleep(1)


# close connection
N1081B_device.disconnect()

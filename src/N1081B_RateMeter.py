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

# login with default password
authorized = N1081B_device.login("password")
if (authorized):

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

    # set section A function as rate meter advanced
    N1081B_device.set_section_function(N1081B.Section.SEC_A,
                                    N1081B.FunctionType.FN_RATE_METER_ADVANCED)

    # set section B function as pulse generator
    N1081B_device.set_section_function(N1081B.Section.SEC_B,
                                    N1081B.FunctionType.FN_PULSE_GENERATOR)

    # configure the Advanced rate meter to integrate for 100ms
    N1081B_device.configure_rate_meter_advanced(N1081B.Section.SEC_A,
                                                True, True, True, True,
                                                False,
                                                False,
                                                0,0,0,0,
                                                N1081B.FilterMode.FILTER_OFF,
                                                N1081B.IntegrationTimeMode.TIME_100ms)

    # configure the pulse generator (Poisson random generator, width:200ns, period: 10000ns, output all enabled)
    N1081B_device.configure_pulse_generator(N1081B.Section.SEC_B,
                                            N1081B.StatisticMode.STAT_POISSON,
                                            200, 10000, True, True, True, True)


    # loop reading the counter values
    old_value = 0
    while 1:
        # use the generic function get_function_results to get the section A result
        counter_json = N1081B_device.get_function_results(N1081B.Section.SEC_A)

        # decode the counter value of channel 0 (section A)
        value = counter_json["data"]["counters"][0]["value"]
        print(str(value) + "    delta: " + str(value-old_value))
        old_value = value
        time.sleep(0.1)

else:
    print("Wrong password!")

# close connection
N1081B_device.disconnect()

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

    # set section A function as time over threshold
    N1081B_device.set_section_function(N1081B.Section.SEC_A,
                                    N1081B.FunctionType.FN_TIME_TAG)

    # set section B function as pulse generator
    N1081B_device.set_section_function(N1081B.Section.SEC_B,
                                    N1081B.FunctionType.FN_PULSE_GENERATOR)

    # configure time tag to acquire from channel 0 only
    N1081B_device.configure_time_tagging(N1081B.Section.SEC_A, True, False, False, False, False, False)

    # configure the pulse generator (Poisson random generator, width:200ns, period: 10000ns, output all enabled)
    N1081B_device.configure_pulse_generator(N1081B.Section.SEC_B,
                                            N1081B.StatisticMode.STAT_POISSON,
                                            2000, 10000000, True, True, True, True)

    # reset acquisition on section A
    N1081B_device.stop_acquisition(N1081B.Section.SEC_A,
                                    N1081B.FunctionType.FN_TIME_TAG)


    # start acquisition on section A
    N1081B_device.start_acquisition(N1081B.Section.SEC_A,
                                    N1081B.FunctionType.FN_TIME_TAG)

    while 1:
        vv = N1081B_device.get_time_tag_data()
        pp.pprint(vv)
    # stop acquisition
    N1081B_device.stop_acquisition(N1081B.Section.SEC_A)

else:
    print("Wrong password!")

# close connection
N1081B_device.disconnect()
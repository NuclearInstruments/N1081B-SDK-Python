# to run this demo connect OUT-B-0 to IN-A-0 with a lemo cable

import pprint
import time
import matplotlib.pyplot as plt
import numpy as np
from N1081B_sdk import N1081B

def my_lines(ax, pos, *args, **kwargs):
    if ax == 'x':
        for p in pos:
            plt.axvline(p, *args, **kwargs)
    else:
        for p in pos:
            plt.axhline(p, *args, **kwargs)

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

    # set input of section A in NIM standard
    response_json = N1081B_device.set_input_configuration(N1081B.Section.SEC_A,
                                                        N1081B.SignalStandard.STANDARD_NIM,
                                                        N1081B.SignalStandard.STANDARD_NIM,
                                                        0, N1081B.SignalImpedance.IMPEDANCE_50)

    # set output of section B in NIM standard
    response_json = N1081B_device.set_output_configuration(N1081B.Section.SEC_B,
                                                        N1081B.SignalStandard.STANDARD_NIM)

    # set section A function as counter
    response_json = N1081B_device.set_section_function(N1081B.Section.SEC_A,
                                                    N1081B.FunctionType.FN_COUNTER)

    # set section B function as pulse generator
    response_json = N1081B_device.set_section_function(N1081B.Section.SEC_B,
                                                    N1081B.FunctionType.FN_PULSE_GENERATOR)

    # configure the pulse generator (width:200ns, period: 10000ns, output all enabled)
    response_json = N1081B_device.configure_pulse_generator(N1081B.Section.SEC_B,
                                                            N1081B.StatisticMode.STAT_DETERMINISTIC,
                                                            200, 1000, True, True, True, True)

    # configure the trigger of the logic analyser
    N1081B_device.set_logic_analyzer_trigger(N1081B.LogicAnalyzerTriggerMode.LA_TRIGGER_OR, N1081B.LogicAnalyzerTriggerMode.LA_TRIGGER_OFF,
                                            N1081B.LogicAnalyzerTriggerEdge.LA_EDGE_RISING,
                                            True, False, False, False, False, False,
                                            False, False, False, False,
                                            False, False, False, False, False, False,
                                            False, False, False, False,
                                            False,False,False,False,False,False,
                                            False, False, False, False,
                                            False,False,False,False,False,False,
                                            False, False, False, False,
                                            )

    # start logic analyser acquisition
    N1081B_device.start_logic_analyzer()

    # give time to the logic analyser to be triggered
    time.sleep(0.1)

    # download the data
    waves = N1081B_device.get_logic_analyzer_data()

    # extract data of channel 0 section A
    channel_A_0 = waves["data"]["inputs"][0]


    # plot clock and signal
    data = np.repeat(channel_A_0, 2)
    clock = 1 - np.arange(len(data)) % 2

    t = 0.5 * np.arange(len(data))


    my_lines('y', [0, 2], color='.5', linewidth=2)
    plt.step(t, clock + 2, 'r', linewidth = 2, where='post')
    plt.step(t, data + 0, 'r', linewidth = 2, where='post')

    plt.ylim([-0.1,4.5])

    for tbit, bit in enumerate(channel_A_0):
        plt.text(tbit, 1, str(bit))

    plt.gca().axis('off')
    plt.show()

else:
    print("Wrong password!")

 # close connection
N1081B_device.disconnect()
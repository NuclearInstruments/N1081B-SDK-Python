import pprint
import time
import matplotlib.pyplot as plt
from N1081A_sdk import N1081B

pp = pprint.PrettyPrinter(indent=4)

N1081A_device = N1081B("192.168.50.5")
version_json = N1081A_device.get_version()
pp.pprint(version_json)
serial_number = version_json["data"]["serial_number"]
software_version = version_json["data"]["software_version"]
zynq_version = version_json["data"]["zynq_version"]
fpga_version = version_json["data"]["fpga_version"]

response_json = N1081A_device.set_section_function(N1081B.Section.SEC_A, N1081B.FunctionType.FN_COUNTER)
pp.pprint(response_json)
response_json = N1081A_device.set_section_function(N1081B.Section.SEC_B, N1081B.FunctionType.FN_PULSE_GENERATOR)
pp.pprint(response_json)

response_json = N1081A_device.configure_pulse_generator(N1081B.Section.SEC_B, N1081B.StatisticMode.STAT_DETERMINISTIC, 200, 10000, True, True, True, True)
pp.pprint(response_json)


old_value = 0
while 1:
    counter_json = N1081A_device.get_function_results(N1081B.Section.SEC_A)
    
    value = counter_json["data"]["counters"][0]["value"]
    print(str(value) + "    delta: " + str(value-old_value)) 
    old_value = value
    time.sleep(1)

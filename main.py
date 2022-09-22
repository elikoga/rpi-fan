import gpiod
import json
import subprocess
import time


def get_temp():
    temp = subprocess.check_output(["sensors", "-j"])
    temp = json.loads(temp)
    return temp["cpu_thermal-virtual-0"]["temp1"]["temp1_input"]


chip = gpiod.Chip("gpiochip0")
line = chip.get_line(14)
try:
    line.request(consumer="fan-control")
    histeresis_low = 50
    histeresis_high = 55
    while True:
        temp = get_temp()
        if temp > histeresis_high:
            line.set_value(1)
        elif temp < histeresis_low:
            line.set_value(0)
        time.sleep(10)
finally:
    line.set_value(1)  # default to on
    line.release()

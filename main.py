import gpiod
import json
import subprocess
import time

# get args: --low --high --average_secs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--low", type=float, default=50)
parser.add_argument("--high", type=float, default=65)
parser.add_argument("--average_samples", type=float, default=5)
parser.add_argument("--sample_interval", type=float, default=1)
args = parser.parse_args()


temps = []


def get_temp():
    temp = subprocess.check_output(["sensors", "-j"])
    temp = json.loads(temp)
    temp = temp["cpu_thermal-virtual-0"]["temp1"]["temp1_input"]
    global temps
    temps = temps[-(args.average_samples - 1) :]
    temps.append(temp)
    return sum(temps) / len(temps)


chip = gpiod.Chip("gpiochip0")
line = chip.get_line(14)
try:
    line.request(consumer="fan-control")
    histeresis_low = args.low
    histeresis_high = args.high
    while True:
        temp = get_temp()
        if temp > histeresis_high:
            line.set_value(1)
        elif temp < histeresis_low:
            line.set_value(0)
        time.sleep(args.sample_interval)
finally:
    line.set_value(1)  # default to on
    line.release()

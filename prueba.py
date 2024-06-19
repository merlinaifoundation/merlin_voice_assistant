import sys

import time


def pins_export(pin):
    try:
        pin1export = open("/sys/class/gpio/export", "w")
        pin1export.write(str(pin))
        pin1export.close()
    except IOError:
        print("INFO: GPIO "+str(pin)+" already exists, skipping export")

    fp1 = open("/sys/class/gpio/gpio"+str(pin)+ "/direction", "w")
    fp1.write("out")
    fp1.close()


def write_led(pin,value):
    fp2 = open("/sys/class/gpio/gpio"+str(pin)+ "/value", "w")
    fp2.write(str(value))
    fp2.close()


try:
    
    pins_export(11)
    pins_export(3)
    pins_export(7)

    while True:
        print("on")

        write_led(3,1)
        write_led(11,1)
        write_led(7,1)
        time.sleep(1)
        print("off")
        write_led(3,0)
        write_led(11,0)
        write_led(7,0)
        time.sleep(1)

except Exception as error:
    print(error)

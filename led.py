import machine
import utime
 
led_red = machine.Pin(17, machine.Pin.OUT)
while True:
    led_red.value(1)
    utime.sleep(0.5)
    led_red.value(0)
    utime.sleep(0.5)
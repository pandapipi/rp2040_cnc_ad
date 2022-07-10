from machine import Pin, Timer

led = Pin(25, Pin.OUT)
tim1 = Timer()
tim2 = Timer()
def tick1(timer):
    global led
    led.on()
    tim1.deinit()
def tick2(timer):
    global led
    led.off()
tim1.init(freq=1000, mode=Timer.ONE_SHOT, callback=tick1)
#total period
tim2.init(freq=10000, mode=Timer.PERIODIC, callback=tick2)
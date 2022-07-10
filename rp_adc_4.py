from machine import Pin, Timer,ADC
import utime
led = machine.Pin(0, Pin.OUT)
led.value(0)
def tick(timer):
    global led
    led.toggle()
    
class user_adc:

    conversion_factor = 3.3 / (65535)
    basearray = [0,0,0,0,0,0,0,0,0,0]
    myarray =basearray
    channal = 1
    def __init__(self):
        self.sensor_1 = machine.ADC(26)
        self.sensor_2 = machine.ADC(27)
        self.sensor_3 = machine.ADC(28)
        self.sensor_4 = machine.ADC(29)
        
        
    #how check the channal change

    def get_average(self):
        sum = 0
        for d1 in self.myarray:
            sum = sum +  d1
        return sum/len(self.myarray)
    #定义中断程序
	#定义中断函数，中断函数需要一个定时器输入变量即可，
    def adc_convert(self,tim):
        reading = 0
        if (self.channal == 1):
            reading = self.sensor_1.read_u16() * self.conversion_factor
        if (self.channal == 2):
            reading = self.sensor_2.read_u16() * self.conversion_factor
        if (self.channal == 3):
            reading = self.sensor_3.read_u16() * self.conversion_factor
        if (self.channal == 4):
            reading = self.sensor_4.read_u16() * self.conversion_factor
        self.myarray[:-1] = self.myarray[1:]
        self.myarray[-1] = reading
        # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
        # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
        #temperature = 27 - (reading - 0.706) / 0.001721
        #print(self.myarray)
        print(self.get_average())
        # utime.sleep(2)
if __name__ == '__main__':
    uad = user_adc()
    t = machine.Timer()
    t.init(period=1000, mode=machine.Timer.PERIODIC, callback = uad.adc_convert)
    '''while True:
        utime.sleep(2)
        uad.adc_convert(1)
        print(ub.mean(uad.myarray))'''
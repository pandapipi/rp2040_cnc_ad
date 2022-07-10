import machine
import utime
class nca9555:
    def __init__(self):
        sda=machine.Pin(18)
        scl=machine.Pin(19)
        self.i2c=machine.I2C(1,sda=sda, scl=scl, freq=400000)

    #i2c.writeto(0, '\x7C') #enter settings mode
    def scan(self):
        devices = self.i2c.scan()
        print(devices)#.encode('utf-8'))
        if devices:
            for d in devices:
                print(d)#.encode('utf-8'))
                utime.sleep(1)
    def config(self):

        #config only one paremete

        self.i2c.writeto_mem(0x20, 0x06, b'\x00')
        self.i2c.writeto_mem(0x20, 0x07, b'\x00')
    #portdata is 16bitdata
    def writeport(self,portdata):
        data_byte = portdata.to_bytes(2,'little')
        #byteay = bytes.fromhex(portdata)
        #print(c)
        #print(d)
        c = data_byte[0].to_bytes(1,'little')
        d = data_byte[1].to_bytes(1, 'little')
        self.i2c.writeto_mem(0x20, 0x02, c)
        self.i2c.writeto_mem(0x20, 0x03, d)
        #self.i2c.writeto_mem(0x20, 0x02, b'\x0f')
        #self.i2c.writeto_mem(0x20, 0x03, b'\xf0')
if __name__ == '__main__':
    uic = nca9555()
    uic.scan()
    uic.config()
    uic.writeport(0x0ff0)
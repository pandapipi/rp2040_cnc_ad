from machine import UART, Pin
import time
cfg0 = Pin(21, Pin.OUT) #设置GP15为输出模式
#uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
cfg0.value(0)
time.sleep(1)


txData = b'x55'
txData = txData + b'xaa'
txData = txData + b'x5a'
print(txData)
uart0.write(txData)

rxData = bytes()
while True:
    while uart0.any() > 0:
        rxData += uart0.read(1)
        print(rxData.decode('utf-8'))
    time.sleep(0.1)
    
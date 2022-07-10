from machine import UART, Pin
import time

#uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

txData = b'hello world\n\r'
uart0.write(txData)
time.sleep(0.1)
rxData = bytes()
while True:
    while uart0.any() > 0:
        rxData += uart0.read(1)

    print(rxData.decode('utf-8'))
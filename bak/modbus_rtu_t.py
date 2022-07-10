import time
from machine import UART, Pin
from modbus import ModbusRTU
from rp_i2c import nca9555
from rp_pico_pulse import PIOPWM
uart = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))
modbus = ModbusRTU(uart,slave_id=0x01, register_num=9999)

newdataflag = modbus.REGISTER[0]
conditionflag = modbus.REGISTER[1]
runflag = modbus.REGISTER[2]
channal = modbus.REGISTER[3]
pwm_low = modbus.REGISTER[4]
pwm_high = modbus.REGISTER[5]
uic = nca9555()
uic.scan()
uic.config()
uic.writeport(0x00)
while(True):
    if modbus.any():
        #modbus.handle(debug=True)
        print(modbus.any())
        try:
            modbus.handle(debug=True)
            #print(modbus.REGISTER[0])
        except Exception as exc:
           print(str(exc))
    else:
        time.sleep_ms(100)
        if modbus.REGISTER[0] == 1:
            conditionflag = modbus.REGISTER[1]
            runflag = modbus.REGISTER[2]
            channal = modbus.REGISTER[3]
            pwm_low = modbus.REGISTER[4]
            pwm_high = modbus.REGISTER[5]
            modbus.REGISTER[0] = 0
            newdataflag = modbus.REGISTER[0]
            uic.writeport(channal)
            if runflag == 1:
                pwm = PIOPWM(0, 0, max_count = pwm_low + pwm_high, count_freq=10_000_000)  # 10M
                pwm.set(pwm_high)
                pwm.run(True)
                print('pwm run.')
            else:
                pwm.run(False)
            print('set:')
            print(channal)

        
        
        #print('runflag:'+str(runflag))
        #print('modbus.REGISTER[0]:'+str(modbus.REGISTER[0]))
        #modbus.REGISTER[0] = 1000
        #modbus.REGISTER[1] += 1
        #modbus.REGISTER[3] += 3
        #print(modbus.REGISTER[10:15])
        # image processing in there
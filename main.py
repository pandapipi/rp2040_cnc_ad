
import time
from machine import UART, Pin,Timer
#from modbus import ModbusRTU
from rp_i2c import nca9555
from rp_pico_pulse import PIOPWM
import check_cmd as ccmd
import id_read as idrd

newdataflag = '1'
conditionflag = '1'
runflag = '0'
channal = '0'
pwm_low = '100'
pwm_high = '0'
# 创建LED对象
led=Pin(25, Pin.OUT)

uart = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))
txData = b'hello world\n\r'
uart.write(txData)
time.sleep(0.1)
rxData = bytes()
save_flag = 0
machineid = idrd.readid(idrd.file)
print(machineid)
rxData = bytes()
pwm = None
uic = nca9555()
uic.scan()
uic.config()
uic.writeport(0x00)
# us = '[S_1000_R4_200_0936]'
# print(ccmd.check_string(us))

# 闪烁回调函数
def twinkle(tim):
    # toggle方法:LED状态翻转
    led.toggle()
def makereponse(regidstring,datastring):
    answerstring = '[M_'+ machineid + '_' + regidstring + '_' + datastring + '_'
    checkcode = ccmd.get_check(answerstring[1:])
    answerstring = answerstring + str(checkcode)
    answerstring = answerstring + ']'
    uart.write(answerstring.encode())
    
# 构建定时器
tim = Timer()
    # tim.init(period, mode, callback)
    # period:周期时间(单位为ms)
    # mode:工作模式，有Timer.ONE_SHOT(执行一次)和Timer.PERIODIC(周期性执行)两种
    # callback:定时器中断的回调函数
tim.init(period=1000, mode=Timer.PERIODIC, callback=twinkle)
while True:

    while uart.any() > 0:
        rxData += uart.read(1)
        start_ms = time.ticks_ms()
        save_flag = 1
        # print(rxData)
    if save_flag == 1:
        # print('start ms:',end ='')
        # print(start_ms)
        # current_ms = time.ticks_ms()
        if time.ticks_diff(time.ticks_ms(), start_ms) > 5:
            #raise TimeoutError
            # print('current ms:', end='')
            # print(current_ms)
            print('handle..')
            save_flag = 2
            if(len(rxData)>2):
                # print(rxData)
                
                # us = rxData.decode('utf-8')
                us = rxData.decode()
                print('handle...')
                print(us)
                if(ccmd.check_string(us)):
                    print('handle....')
                    uhandle_str = us[1:-1]
                    # print(uhandle_str)
                    uhandle_array = uhandle_str.split('_')
                    # print(uhandle_array)
                    if uhandle_array[1] == machineid:
                        if uhandle_array[0] == 'S':

                            if uhandle_array[2] == 'R0':
                                machineid = uhandle_array[3]
                                print('set ok')
                                # print(machineid)
                                idrd.writeid(idrd.file,machineid)
                                makereponse(uhandle_array[2], machineid)

                            if uhandle_array[2] == 'R1':
                                runflag = uhandle_array[3]
                                makereponse(uhandle_array[2], runflag)
                                if runflag == '1':
                                    print('pwm run.')
                                    pwm = PIOPWM(0, 0, max_count=int(pwm_low) + int(pwm_high), count_freq=10_000_000)  # 10M
                                    pwm.set(int(pwm_high))
                                    pwm.run(True)

                                else:
                                    if pwm is not None:
                                        pwm.run(False)
                                        print('pwm:stop')
                            if uhandle_array[2] == 'R2':
                                channal = uhandle_array[3]
                                makereponse(uhandle_array[2], channal)
                                int_tmp = 0x00
                                try:
                                    int_tmp = int(channal)

                                    print('channal set:'+str(int_tmp))
                                    uic.writeport(int_tmp)
                                except Exception as exc:
                                    print(str(exc))
                            if uhandle_array[2] == 'R3':
                                pwm_high = uhandle_array[3]
                                makereponse(uhandle_array[2], pwm_high)
                            if uhandle_array[2] == 'R4':
                                pwm_low = uhandle_array[3]
                                makereponse(uhandle_array[2], pwm_low)

                        if uhandle_array[0] == 'R':
                            # print('change id no')
                            if uhandle_array[2] == 'R0':
                                makereponse(uhandle_array[2],machineid)

                            if uhandle_array[2] == 'R1':
                                makereponse(uhandle_array[2], runflag)

                            if uhandle_array[2] == 'R2':
                                makereponse(uhandle_array[2], channal)

                            if uhandle_array[2] == 'R3':
                                makereponse(uhandle_array[2], pwm_high)

                            if uhandle_array[2] == 'R4':
                                makereponse(uhandle_array[2], pwm_low)


                    # else:
                    #     print('idle')
            rxData = b''
            save_flag = 0
        
                                                                                                                                     
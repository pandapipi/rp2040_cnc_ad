from machine import UART, Pin
import _thread
import time
import uModBusConst as Const
import struct
import uModBusFunctions as functions
#from umodbus.uModBusSerial import uModBusSerial

#uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
class uu_modbbus:
    def __init__(self,uart_id, baudrate=9600, data_bits=8, stop_bits=1, parity=None, pins=None):
        pinsLen=len(pins)
        if pins==None or pinsLen<2 or pinsLen>4 or pinsLen==3:
            raise ValueError('pins should contain pin names/numbers for: tx, rx')
        tx=pins[0]
        rx=pins[1]
        self._uart = UART(uart_id, baudrate=baudrate, bits=data_bits, parity=parity,
                          stop=stop_bits, timeout_char=10, tx=tx, rx=rx)
        # uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
    def _calculate_crc16(self, data):
        crc = 0xFFFF

        for char in data:
            crc = (crc >> 8) ^ Const.CRC16_TABLE[((crc) ^ char) & 0xFF]

        return struct.pack('<H',crc)
    def _bytes_to_bool(self, byte_list):
        bool_list = []
        for index, byte in enumerate(byte_list):
            bool_list.extend([bool(byte & (1 << n)) for n in range(8)])

        return bool_list

    def _to_short(self, byte_array, signed=True):
        response_quantity = int(len(byte_array) / 2)
        fmt = '>' + (('h' if signed else 'H') * response_quantity)

        return struct.unpack(fmt, byte_array)
    def _uart_read(self):
        response = bytearray()

        for x in range(1, 40):
            if self._uart.any():
                response.extend(self._uart.read())
                #response.extend(self._uart.readall())
                # variable length function codes may require multiple reads
                if self._exit_read(response):
                    break
            time.sleep(0.05)

        return response
    def _send_receive(self, modbus_pdu, slave_addr, count):
        serial_pdu = bytearray()
        serial_pdu.append(slave_addr)
        serial_pdu.extend(modbus_pdu)

        crc = self._calculate_crc16(serial_pdu)
        serial_pdu.extend(crc)
        self._uart.write(serial_pdu)

    def read_coils(self, slave_addr, starting_addr, coil_qty):
        modbus_pdu = functions.read_coils(starting_addr, coil_qty)

        resp_data = self._send_receive(modbus_pdu, slave_addr, True)
        status_pdu = self._bytes_to_bool(resp_data)

        return status_pdu

    def read_discrete_inputs(self, slave_addr, starting_addr, input_qty):
        modbus_pdu = functions.read_discrete_inputs(starting_addr, input_qty)

        resp_data = self._send_receive(modbus_pdu, slave_addr, True)
        status_pdu = self._bytes_to_bool(resp_data)

        return status_pdu

    def read_holding_registers(self, slave_addr, starting_addr, register_qty, signed=True):
        modbus_pdu = functions.read_holding_registers(starting_addr, register_qty)

        resp_data = self._send_receive(modbus_pdu, slave_addr, True)
        register_value = self._to_short(resp_data, signed)

        return register_value

    def read_input_registers(self, slave_addr, starting_address, register_quantity, signed=True):
        modbus_pdu = functions.read_input_registers(starting_address, register_quantity)

        resp_data = self._send_receive(modbus_pdu, slave_addr, True)
        register_value = self._to_short(resp_data, signed)

        return register_value

    def write_single_coil(self, slave_addr, output_address, output_value):
        modbus_pdu = functions.write_single_coil(output_address, output_value)

        resp_data = self._send_receive(modbus_pdu, slave_addr, False)
        operation_status = functions.validate_resp_data(resp_data, Const.WRITE_SINGLE_COIL,
                                                        output_address, value=output_value, signed=False)

        return operation_status

    def write_single_register(self, slave_addr, register_address, register_value, signed=True):
        modbus_pdu = functions.write_single_register(register_address, register_value, signed)

        resp_data = self._send_receive(modbus_pdu, slave_addr, False)
        operation_status = functions.validate_resp_data(resp_data, Const.WRITE_SINGLE_REGISTER,
                                                        register_address, value=register_value, signed=signed)

        return operation_status

    def write_multiple_coils(self, slave_addr, starting_address, output_values):
        modbus_pdu = functions.write_multiple_coils(starting_address, output_values)

        resp_data = self._send_receive(modbus_pdu, slave_addr, False)
        operation_status = functions.validate_resp_data(resp_data, Const.WRITE_MULTIPLE_COILS,
                                                        starting_address, quantity=len(output_values))

        return operation_status

    def write_multiple_registers(self, slave_addr, starting_address, register_values, signed=True):
        modbus_pdu = functions.write_multiple_registers(starting_address, register_values, signed)

        resp_data = self._send_receive(modbus_pdu, slave_addr, False)
        operation_status = functions.validate_resp_data(resp_data, Const.WRITE_MULTIPLE_REGISTERS,
                                                        starting_address, quantity=len(register_values))

        return operation_status

# txData = b'hello world\n\r'
# uart0.write(txData)
# time.sleep(0.1)
# rxData = bytes()
# while True:
#     while uart0.any() > 0:
#         rxData += uart0.read(1)
#
#     print(rxData.decode('utf-8'))

    def thread_com_receive(self):
        while True:
            try:
                rxData = bytes()
                while self._uart.any() > 0:
                    rxData += self.uart0.read(1)
                time.sleep(0.01)
                print(rxData)
                rxData = bytes()
            except Exception as e:
                pass
                # self.serial_close()
            if self.rev_run_flag == False:
                break
    def run(self):
        self.thread1 = _thread.Thread(target=self.thread_com_receive)
        self.thread1.start()
if __name__ == '__main__':
    my_serial = uu_modbbus(0, baudrate=9600, Pins=(Pin(16), Pin(17)))
    my_serial.run()




#$S_I2_R1_1000_xxxx$
def get_check(input_string):
    abyte = input_string.encode('utf-8')
    sum = 0
    for item in abyte:
        sum = sum + item
    return sum % 10000

def check_string(input_string):
    summ = input_string[-4:]
    print summ
if __name__ == '__main__':
    check_string('$S_I2_R1_1000_xxxx$')

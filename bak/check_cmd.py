
#$S_I2_R1_1000_xxxx$
import re


def RegularExpression(input_string):
    uformat = '\A$'
    result = re.match(uformat,input_string)
    if result:
        print("Search successful.")
    else:
        print("Search unsuccessful.")
def get_check(input_string):
    try:
        #print(input_string)
        abyte = input_string.encode('utf-8')
        #print(abyte)
        sum = 0
        for item in abyte:
            #print(item)
            sum = sum + item
        #print(sum)
        return sum % 10000
    except Exception as exc:
        print(str(exc))
        return 0

def check_string(input_string):
    fomat = '/$S_I[0-9]*_R[0-9]*_R[0-9]*_R[0-9]*$/'
    try:
        summ = int(input_string[-5:-1])
        print(summ)
        sum = get_check(input_string[1:-5])

        print(summ)
        return summ == sum
    except Exception as exc:
        print(str(exc))
        return False
if __name__ == '__main__':
    #print(check_string('$S_I2_R1_1000_0910$'))
    #RegularExpression('$S_I2_R1_1000_0910$')
    pattern = '\Athe'
    test_string = 'the sun]['
    result = re.match(pattern, test_string)

    if result:
        print("Search successful.")
    else:
        print("Search unsuccessful.")


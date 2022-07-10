file = 'id.txt'
def readid(input_file):
    try:
        f = open(input_file,'r')
        line = f.readline()
        f.close()
        return line
    except Exception as exc:
        print(str(exc))
        return None
def writeid(input_file,idstring):
    try:
        f = open(input_file,'w')
        f.write(idstring)
        f.close()
        return True
    except Exception as exc:
        print(str(exc))
        return False
if __name__ == '__main__':
    writeid(file,'abcdc')
    print(readid(file))
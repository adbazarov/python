import sys
CMD={'a':1,
    'b':2
    }
def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)


BIAS=7
REFO=6
DF=5
UB=4
BD=3
MSB=2
SDL=1
DRDY=0
CMD1=0
CMD1=set_bit(CMD1,BIAS)
print(CMD1)

print(CMD['a'])

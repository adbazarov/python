import spidev
import RPi.GPIO as GPIO
import time
CS_PIN_ADC1 = 25
DRDY_PIN = 8

RST_PIN = 7
CS={
        'ADC1':25,
        'ADC2':24,
        'ADC3':23
}
DRDY={
        'ADC1': 8,
        'ADC2': 22,
        'ADC3': 27
}
CMD = {'RD_DATA': 0xC0,     # Completes SYNC and Exits Standby Mode 0000  0000 (00h)
       'WR_CMD' : 0x64,      # Read Data 0000  0001 (01h)
       'RD_CMD' : 0xE4,     # Read Data Continuously 0000   0011 (03h)
       'RD_OCR' : 0xE4     # Stop Read Data Continuously 0000   1111 (0Fh)
      }
Calibration={
    'Self-calibration':0b001,
    'Offset-calibration':0b010,
    'Full-Scale Calibration':0b11,
    'Predo-System-calibration':0b100,
    'Background-calibration':0b101,
}

class ADS1210:
    def __init__(self):
        def self_test_adc():
            reset_adc()
            digital_write(CS_PIN, 0)
            spi_writebyte(5)
            spi_writebyte(32)
            digital_write(CS_PIN, 1)
            

        def wait_DRY():
            for i in range(0, 40000, 1):
                if (digital_read(DRDY_PIN) == 0):
                    break
            if (i >= 39000):
                print('Time out wait DRDY!')

        def init_adc():
            CMD = [0b01000010,0x00, 0x00, 0x4D]
            reset_adc()
            digital_write(CS_PIN, 0)
            wait_DRY()
            spi_writebyte(WR_CMD)
            delay_ms(1)
            spi_writebyte(CMD[0])
            spi_writebyte(CMD[1])
            spi_writebyte(CMD[2])
            spi_writebyte(CMD[3])
            digital_write(CS_PIN, 1)
            print(CMD)
# end class ADS1210


def digital_write(pin,value):
    GPIO.output(pin,value)

def digital_read(pin):
    return GPIO.input(pin)

def delay_ms(delaytime):
    time.sleep(delaytime//1000.)

def spi_writebyte(data):
    SPI.writebytes([data])

def spi_readbyte(reg):
    return SPI.readbytes(reg)

def module_init():

    GPIO.setmode(GPIO.BCM)
#    GPIO.setwarning(False)
    GPIO.setup(RST_PIN,GPIO.OUT)
    GPIO.setup(CS_PIN,GPIO.OUT)
    GPIO.setup(DRDY_PIN,GPIO.IN)#pull_up_down=GPIO.PUD_UP
    SPI.max_speed_hz=20000
    SPI.mode=0b01
    SPI.no_cs=True

def reset_adc():
    digital_write(RST_PIN,0)
    delay_ms(1)
    digital_write(RST_PIN,1)

def cs_adc(channel):
    digital_write(CS_PIN,0)





#======================================    
print('start adc')
SPI=spidev.SpiDev(0,0)
module_init()
init_adc()
self_test_adc()
delay_ms(1000)
reg=0
for i in range(10000):

    reset_adc()
    wait_DRY()
    digital_write(CS_PIN,0)
    spi_writebyte(RD_DATA)
    delay_ms(1)
    byte_1=spi_readbyte(reg)
    byte_2=spi_readbyte(reg)
    byte_3=spi_readbyte(reg)
    digital_write(CS_PIN,1)
    print(byte_1,byte_2,byte_3,((byte_1[0]<<16)|(byte_2[0]<<8)|(byte_3[0]))-8388608)
    delay_ms(100)





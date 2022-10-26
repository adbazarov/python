import spidev
import RPi.GPIO as GPIO
import time

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
        self.SPI = spidev.SpiDev(0, 0)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RST_PIN, GPIO.OUT)
        GPIO.setup(CS['ADC1'], GPIO.OUT)
        GPIO.setup(DRDY['ADC1'], GPIO.IN)
        self.SPI.max_speed_hz = 20000
        self.SPI.mode = 0b01
        self.SPI.no_cs = True

    def self_test_adc(self):
        self.reset_adc()
        self.digital_write(CS['ADC1'], 0)
        self.spi_writebyte(5)
        self.spi_writebyte(32)
        self.digital_write(CS['ADC1'], 1)


    def wait_DRY(self):
        for i in range(0, 40000, 1):
            if (self.digital_read(DRDY['ADC1']) == 0):
                break
            if (i >= 39000):
                print('Time out wait DRDY!')
                break

    def init_adc(self):
        CMD = [0b01000010,0x00, 0x00, 0x4D]
        self.reset_adc()
        self.digital_write(CS['ADC1'], 0)
        self.wait_DRY()
        self.spi_writebyte(CMD['WR_CMD'])
        self.delay_ms(1)
        self.spi_writebyte(CMD[0])
        self.spi_writebyte(CMD[1])
        self.spi_writebyte(CMD[2])
        self.spi_writebyte(CMD[3])
        self.digital_write(CS['ADC1'], 1)
        print(CMD)

    def module_init(self ):
        print('Init module')

    def reset_adc(self ):
        self.digital_write(RST_PIN, 0)
        self.delay_ms(1)
        self.digital_write(RST_PIN, 1)

    def cs_adc(self, channel):
        self.digital_write(CS['ADC1'], 0)

    def digital_write(self, pin, value):
        GPIO.output(pin, value)

    def digital_read(self, pin):
        return GPIO.input(pin)

    def delay_ms(self, delaytime):
        time.sleep(delaytime // 1000.)

    def spi_writebyte(self, data):
        self.SPI.writebytes([data])

    def spi_readbyte(self, reg):
        return self.SPI.readbytes(reg)
    def read_data(self):
        self.wait_DRY()
        self.digital_write(CS['ADC1'], 0)
        self.spi_writebyte(CMD['RD_DATA'])
        self.delay_ms(1)
        byte_1 = self.spi_readbyte(0x01)
        byte_2 = self.spi_readbyte(0x01)
        byte_3 = self.spi_readbyte(0x01)
        self.digital_write(CS['ADC1'], 1)
        print(byte_1, byte_2, byte_3, ((byte_1[0] << 16) | (byte_2[0] << 8) | (byte_3[0])) - 8388608)

# end class ADS1210









#======================================    
print('start adc')

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





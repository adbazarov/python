import spidev
import RPi.GPIO as GPIO
import time
import threading


#print(GPIO.VERSION)
#spi=spidev.SpiDev(0,0)
#spi.no_cs=False
#spi.bits_per_word=8
#spi.mode=0b01
#spi.lsbfirst=False
#spi.open(0,0)
#spi.max_speed_hz=500000
#txData=[0x01,0x01]
GPIO.setmode(GPIO.BCM)# имена пинов по их номеру GPIO


CS={
    'ADC1':25,
    'ADC2':24,
    'ADC3':23,
    'ADC4':22,
    'ADC5':27    
}

GPIO.setup(CS['ADC5'],GPIO.OUT)



for i in range(1000):
    time.sleep(1) 
    GPIO.output(CS['ADC5'],GPIO.HIGH)
    time.sleep(1)
    GPIO.output(CS['ADC5'],GPIO.LOW)


#    GPIO.output(7,0)

GPIO.cleanup()
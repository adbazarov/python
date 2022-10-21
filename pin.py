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

PIN=27
GPIO.setup(PIN,GPIO.OUT)
GPIO.output(PIN,GPIO.LOW)

for i in range(1000):
    time.sleep(1) 
    GPIO.output(PIN,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(PIN,GPIO.LOW)


#    GPIO.output(7,0)

GPIO.cleanup()
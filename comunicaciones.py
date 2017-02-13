import serial

import time

import RPi.GPIO as GPIO

arduino=serial.Serial('/dev/ttyACM0',115200)

Varrrrr=0.0

GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.OUT)

GPIO.setup(24,GPIO.OUT)

GPIO.output(23,GPIO.HIGH)

GPIO.output(24,GPIO.LOW)

while 1:
	
	try:
	
		while arduino.inWaiting():

			Varrrrr=arduino.readline()
		
			print Varrrrr
			
			Varrrrr=0.0
	
	except KeyboardInterrupt:
	
		GPIO.output(23,GPIO.LOW)

		GPIO.output(24,GPIO.LOW)
	
		GPIO.close()

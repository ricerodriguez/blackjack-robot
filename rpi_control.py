##
## RPI control program
## Aaron Carman
##

import RPi.GPIO as GPIO
from time import sleep

def hit(currentVal):
    GPIO.output(MSP0, True)
    GPIO.output(MSP1, False)
    sleep(0.5)
    GPIO.output(MSP0, False)
    GPIO.output(MSP1, False)
    return newVal

def stay():
    GPIO.output(MSP0, False)
    GPIO.output(MSP1, True)
    sleep(0.5)
    GPIO.output(MSP0, False)
    GPIO.output(MSP1, False)
    return

MSP0 = 10
MSP1 = 11
trigPin = 12

GPIO.setmode(GPIO.BOARD)

GPIO.setup(MSP0, GPIO.OUT)
GPIO.setup(MSP1, GPIO.OUT)
GPIO.setup(trigPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

sleep(0.1)

while True:

    GPIO.output(MSP0, True)
    GPIO.output(MSP1, True)

    sleep(1)
    
    GPIO.output(MSP0, False)
    GPIO.output(MSP1, False)
    
    for i in range(5):
        playval[i] = hit(playval[i])

    dealval = hit(dealval)

    for i in range(5):
        playval[i] = hit(playval[i])

    for i in range(5):
        while True:
            try:
                self.cereal = Serial('dev/ttyUSB0',timeout=1)
                logging.info('SUCCESSFULLY CONNECTED')
                # Connected, now listening for what to do
                cmd_raw = self.cereal.readline()
                cmd = str(cmd_raw)
                if (cmd == 'hit'):
                    GPIO.output(MSP0, True)
                    GPIO.output(MSP1, False)
                    sleep(0.5)
                    GPIO.output(MSP0, False)
                    GPIO.output(MSP1, False)
                elif (cmd == 'double'):
                    GPIO.output(MSP0, True)
                    GPIO.output(MSP1, False)
                    sleep(0.5)
                    GPIO.output(MSP0, False)
                    GPIO.output(MSP1, False)
                    sleep(5)
                    GPIO.output(MSP0, False)
                    GPIO.output(MSP1, True)
                    sleep(1)
                    GPIO.output(MSP0, False)
                    GPIO.output(MSP1, False)
                    
                elif (cmd == 'stay'):
                    GPIO.output(MSP0, False)
                    GPIO.output(MSP1, True)
                    sleep(0.5)
                    GPIO.output(MSP0, False)
                    GPIO.output(MSP1, False)
                else:
                    GPIO.output(P0, False)
                    GPIO.output(P1, False)
                
            except serialutil.SerialException:
                logging.warning('CONNECTION FAILED, TRYING AGAIN')
            ##if received hit:
                playval[i] = hit(playval[i])
            ##elif stay:
                stay()
                break
            ##elif double:
                playval[i] = hit(playval[i])
                stay()
                break

    dealval = hit(dealval)
    sleep(5)

    
    

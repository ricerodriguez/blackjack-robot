##
## RPI control program
## Aaron Carman
##

import RPi.GPIO as GPIO
from time import sleep

def hit(currentVal):
    GPIO.output(MSP0, True)
    GPIO.output(MSP1, False)
    while(GPIO.input(trigPin) == 0):
        sleep(0.001)
    GPIO.output(MSP0, False)
    ## read card in
    newVal = currentVal + 1
    GPIO.output(MSP0, True)
    GPIO.output(MSP1, True)
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

playbank = [500,500,500,500,500]
playbet = [5,5,5,5,5]
playval = [0,0,0,0,0]
dealval = 0

GPIO.setmode(GPIO.BOARD)

GPIO.setup(MSP0, GPIO.OUT)
GPIO.setup(MSP1, GPIO.OUT)
GPIO.setup(trigPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

sleep(0.1)

## wait on MSP430 to put a card in the hole

while True:

    GPIO.output(MSP0, True)
    GPIO.output(MSP1, True)
    
    ## get player bets
    
    GPIO.output(MSP0, False)
    GPIO.output(MSP1, False)
    
    for(i in range(5)):
        playval[i] = hit(playval[i])

    dealval = hit(dealval)

    for(i in range(5)):
        playval[i] = hit(playval[i])

    for(i in range(5)):
        while True:
            ## get info from PUI
            ##if hit:
                playval[i] = hit(playval[i])
            ##elif stay

    dealval = hit(dealval)

    while (dealval < 17):
        dealval = hit(dealval)

    for(i in range(5)):
        if(playval[i] > dealval):
            playbank[i] = playbank[i] + playbet[i]
        elif(playval[i] < dealval):
            playbank[i] = playbank[i] - playbet[i]

    
    

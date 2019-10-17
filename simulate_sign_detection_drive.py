from time import sleep
import random
import RPi.GPIO as GPIO
import os

# Number PINS
GPIO_SIGN_INTERRUPT = 20

GPIO_IS_INFO_SIGN = 21

GPIO_NUMBER_BIT_0 = 26
GPIO_NUMBER_BIT_1 = 19
GPIO_NUMBER_BIT_2 = 13
GPIO_NUMBER_BIT_3 = 6

# Init Pins
GPIO_PI_INIT_DONE = 12
GPIO_CAM_READY = 16
GPIO_ARDUINO_INIT_DONE = 18

# Train state
GPIO_CUBE_STORED = 23
GPIO_TRAIN_STOPPED = 24

# Communication Pins
GPIO_UART_TXD = 14
GPIO_UART_RXT = 15

# Falgs to toggle
arduinoReadyActivated = False
cubeStoredActivated = False

# Simulated signs
simulated_info_signal = 6
simulated_signs = [{
        "number": 8,
        "timeTillNext": 3
    },
    {
        "number": 3,
        "timeTillNext": 2
    },
    {
        "number": 6,
        "timeTillNext": 3
    },
    {
        "number": 1,
        "timeTillNext": 1
    }]


def printArduinoReady():
    print("Arduino ready!")
    arduinoReadyActivated = True

def printCubeStored():
    print("Cube stored!")
    cubeStoredActivated = True

def printTrainStopped():
    GPIO.add_event_detect(GPIO_ARDUINO_INIT_DONE, GPIO.RISING, callback=printArduinoReady)
    GPIO.add_event_detect(GPIO_CUBE_STORED, GPIO.RISING, callback=printCubeStored)
    GPIO.add_event_detect(GPIO_TRAIN_STOPPED, GPIO.RISING, callback=printTrainStopped)

def initGPIOs():
    print("Start init")
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)  

    GPIO.setup(GPIO_NUMBER_BIT_0, GPIO.OUT)
    GPIO.setup(GPIO_NUMBER_BIT_1, GPIO.OUT)
    GPIO.setup(GPIO_NUMBER_BIT_2, GPIO.OUT)
    GPIO.setup(GPIO_NUMBER_BIT_3, GPIO.OUT)
    GPIO.setup(GPIO_IS_INFO_SIGN, GPIO.OUT)
    GPIO.setup(GPIO_SIGN_INTERRUPT, GPIO.OUT)
    GPIO.setup(GPIO_PI_INIT_DONE, GPIO.OUT)
    GPIO.setup(GPIO_CAM_READY, GPIO.OUT)
    GPIO.setup(GPIO_ARDUINO_INIT_DONE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_CUBE_STORED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_TRAIN_STOPPED, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(GPIO_UART_TXD, GPIO.OUT)
    GPIO.setup(GPIO_UART_RXT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(GPIO_ARDUINO_INIT_DONE, GPIO.RISING, callback=printArduinoReady)
    GPIO.add_event_detect(GPIO_CUBE_STORED, GPIO.RISING, callback=printCubeStored)
    GPIO.add_event_detect(GPIO_TRAIN_STOPPED, GPIO.RISING, callback=printTrainStopped)

    print("Init done\n")



def sendDetectedSign(number, isInfoSign):
    print("Sign: %d" % number)
    
    # Calculate bits
    bit0 = (number & 1) == 1
    number = int(number / 2)
    print("Bit 0 set to %d, number= %d" % (bit0, number))

    bit1 = (number & 1) == 1
    number = int(number / 2)
    print("Bit 1 set to %d, number= %d" % (bit1, number))

    bit2 = (number & 1) == 1
    number = int(number / 2)
    print("Bit 2 set to %d, number= %d" % (bit2, number))

    bit3 = (number & 1) == 1
    number = int(number / 2)
    print("Bit 3 set to %d, number= %d" % (bit3, number))

    print("Sending following bit combination: %d%d%d%d - Is Info Sign: %d" % (bit3, bit2, bit1, bit0, isInfoSign))

    # Send interrupt
    GPIO.output(GPIO_NUMBER_BIT_0, bit0)
    GPIO.output(GPIO_NUMBER_BIT_1, bit1)
    GPIO.output(GPIO_NUMBER_BIT_2, bit2)
    GPIO.output(GPIO_NUMBER_BIT_3, bit3)
    GPIO.output(GPIO_IS_INFO_SIGN, isInfoSign)
    GPIO.output(GPIO_SIGN_INTERRUPT, True)
    sleep(0.05)

    # Reset pins
    GPIO.output(GPIO_NUMBER_BIT_0, False)
    GPIO.output(GPIO_NUMBER_BIT_1, False)
    GPIO.output(GPIO_NUMBER_BIT_2, False)
    GPIO.output(GPIO_NUMBER_BIT_3, False)
    GPIO.output(GPIO_IS_INFO_SIGN, False)
    GPIO.output(GPIO_SIGN_INTERRUPT, False)   
    



def driveOneRound(i):
    print("***************************")
    print("**** Drive round Nr: %d ****" % i)
    print("***************************")
    print("Info sign detected with Nr: %d" % simulated_info_signal)
    sendDetectedSign(simulated_info_signal, True)
    input()
    #sleep(2)
    for sign in simulated_signs:
        print("Stop sign detected with Nr: %d" % sign["number"])
        sendDetectedSign(sign["number"], False)
        print("[Time till next sign: %d]" % sign["timeTillNext"])

        print("Press enter for the next sign...")
        input()
        #sleep(sign["timeTillNext"])
    print("\n\n")

#while cubeStoredActivated is False:
#    print("Wait till cube is stored...")
#    sleep(1)
try:
    initGPIOs()

    print("Wait 5 Seconds before start")
    input()
    #sleep(5)

    for i in range(0, 3):
        driveOneRound(i)
except KeyboardInterrupt:
  GPIO.cleanup()
  print("Bye")

GPIO.cleanup()

import RPi.GPIO as GPIO
import time

used_gpios = [11, 12, 13]

def my_callback(channel):
    print('Edge detected on channel %s with value %i' % (channel, GPIO.input(channel)))
    print('This is run in a different thread to your main program')


# Use this to use the enumeration of the GPIOs themselve (GPIO14, GPIO15 etc.)
# GPIO.setmode(GPIO.BCM)  

# Use this to use the board enumeration (P1, P2, P3 etc.)
GPIO.setmode(GPIO.BOARD)  

for channel in used_gpios:
    print("SetupPIN %i with pull-down-resistor" % channel)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback)  # add rising edge detection on a channel
    #GPIO.add_event_detect(channel, GPIO.FALLING, callback=my_callback)  # add falling edge detection on a channel

counter = 0
try:
    while True:
        print("Programm runs since %i seconds" % counter)
        print("Current channel state: ")
        for channel in used_gpios:
             print('-> Channel %s with state %i' % (channel, GPIO.input(channel)))   
        print("\n")
        time.sleep(1)
        counter += 1

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Bye")
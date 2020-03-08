#Libraries
import RPi.GPIO as GPIO
import time
import keyboard

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_TRIGGER1 = 19
GPIO_ECHO = 24
GPIO_ECHO1 = 23

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)

def distance(gptrig, gpecho):
    # set Trigger to HIGH
    GPIO.output(gptrig, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(gptrig, False)
    StartTime = time.time()
    StopTime = time.time()


    while GPIO.input(gpecho) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(gpecho) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    return distance

#Media Functions
def pp():
    keyboard.press_and_release(' ')
def forwards():
    keyboard.press_and_release('right')
def backwards():
    keyboard.press_and_release('left')

#0 = Undetected, 1 = Left Detected, 2 = Right Detected
state = 0
delta1 = time.time()

if __name__ == '__main__':
    try:
        while True:
            #Determines time passed
            dist2 = distance(GPIO_TRIGGER1, GPIO_ECHO1)
            time.sleep(0.08)
            dist1 = distance(GPIO_TRIGGER, GPIO_ECHO)
            delta2 = time.time() - delta1
#           print (dist1)
#           print (dist2)
            #Initial detection
            #Right Side
            if dist1 < 15 and dist2 > 15 and state == 0:
                state = 1
                delta1 = time.time()
            #Left Side
            elif dist1 > 15 and dist2 < 15 and state == 0:
                state = 2
                delta1 = time.time()

            #Right to Left
            if dist1 > 15 and dist2 < 15 and delta2 < 1.2 and state == 1:
                state = 0
        	backwards()
                time.sleep(0.25)
            #Left to Right
            elif dist1 < 15 and dist2 > 15 and delta2 < 1.2 and state == 2:
                state = 0
                forwards()
                time.sleep(0.25)
	    #Pause/Play
            elif dist1 < 15 and dist2 < 15 and delta2 > 1.2 and state != 0:
                pp()
                state = 0
                time.sleep(0.25)

            #Reset outside of range
            elif dist1 > 15 and dist2 > 15:
                state = 0
            #Update time 1 when not detecting
            if state == 0:
                delta1 = time.time()

            time.sleep(0.05)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
	print("Measurement stopped by User")
        GPIO.cleanup()






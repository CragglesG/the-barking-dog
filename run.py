import RPi.GPIO as GPIO
from picamera2 import Picamera2 as picam
import subprocess
from time import sleep
from playsound import playsound


# Set up GPIO pins
GPIO.setmode(GPIO.BCM)    
PIR_PIN = 10
GPIO.setup(PIR_PIN, GPIO.IN)

cam = picam()

config = cam.create_still_configuration()

def main(pir):
    # Main loop
    while True:
        if GPIO.input(pir):
            print("Movement detected!")
            break

try:
    while True:
        main(PIR_PIN)
        cam.start()
        sleep(1)
        cam.switch_mode_and_capture_file(config, "image.jpg")
        subprocess.run(["python3", "identify.py"])
        with open("result.txt", "r") as result:
            res = result.read()
            if res == 'y':
                print('RABBIT DETECTED!!! BARK DOG, BARK!!!')
                playsound("./dog-barking-70772.mp3")
            else:
                print('No rabbits')

except KeyboardInterrupt:
    GPIO.cleanup()

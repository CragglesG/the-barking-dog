import RPi.GPIO as GPIO
from picamera2 import Picamera2 as picam
import subprocess
from time import sleep
from playsound import playsound


# Set up GPIO pins
GPIO.setmode(GPIO.BOARD)    
PIR_PIN = 2
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
        cam.close()
        subprocess.run(["python3", "identify.py"])
        with open("result.txt", "r") as result:
            res = result.read()
            if res == 'y':
                playsound("./dog-barking-70772.mp3")

except KeyboardInterrupt:
    GPIO.cleanup()
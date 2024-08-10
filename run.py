from gpiozero import MotionSensor
from picamera2 import Picamera2 as picam
import subprocess
from time import sleep
from playsound import playsound


pir = MotionSensor(15)

cam = picam()

config = cam.create_still_configuration()

def main(pir: MotionSensor):
    # Main loop
    while True:
        pir.wait_for_active()
        print("Movement detected!")
        break

try:
    while True:
        main(pir)
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
    cam.close()

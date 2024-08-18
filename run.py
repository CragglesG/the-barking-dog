import RPi.GPIO as gpio
from picamera2 import Picamera2 as picam
from time import sleep
from playsound import playsound
from PIL import Image

import torch
from torchvision import models, transforms
from labels import classes

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

net = models.quantization.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
net = torch.jit.script(net)

gpio.setmode(gpio.BCM)
gpio.setup(12,gpio.IN)

cam = picam()
config = cam.create_still_configuration()

def identify(img: Image):
    with torch.no_grad():
        input_tensor = preprocess(img)

        input_batch = input_tensor.unsqueeze(0)

        output = net(input_batch)

        top = list(enumerate(output[0].softmax(dim=0)))
        top.sort(key=lambda x: x[1], reverse=True)
        for idx, val in top[:10]:
            if classes[idx] in ['hare', 'wood rabbit, cottontail, cottontail rabbit', 'Angora, Angora rabbit']:
                return True
            else:
                return False

def main():
    while True:
        if gpio.input(12):
            print("Movement detected!")
            break

try:
    while True:
        main()
    
        cam.start()
        sleep(1)
        img = cam.switch_mode_and_capture_image(config)

        res = identify(img)
        if res:
            print('RABBIT DETECTED!!! BARK DOG, BARK!!!')
            playsound("./dog-barking-70772.mp3")
        else:
            print('No rabbits')
except KeyboardInterrupt:
    cam.close()

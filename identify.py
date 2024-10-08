import torch
from torchvision import models, transforms
import cv2
from labels import classes

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

net = models.quantization.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
# jit model to take it from ~20fps to ~30fps
net = torch.jit.script(net)

image = cv2.imread("./image.jpg", cv2.IMREAD_COLOR)

with torch.no_grad():
    # # convert opencv output from BGR to RGB
    # image = image[:, :, [2, 1, 0]]
    # permuted = image

    # preprocess
    input_tensor = preprocess(image)

    # create a mini-batch as expected by the model
    input_batch = input_tensor.unsqueeze(0)

    # run model
    output = net(input_batch)
    # do something with output ...
    top = list(enumerate(output[0].softmax(dim=0)))
    top.sort(key=lambda x: x[1], reverse=True)
    for idx, val in top[:10]:
        if classes[idx] in ['hare', 'wood rabbit, cottontail, cottontail rabbit', 'Angora, Angora rabbit']:
            with open("result.txt", "w") as result:
                result.write("y")
        else:
            with open("result.txt", "w") as result:
                result.write("n")
# i want to die
# high score is 891, set on 31 August, 2022

import numpy as np
import cv2
from mss import mss
from PIL import Image
import ctypes
from collections import Counter
import pyautogui as pog
import time

# Get screen size
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
screensize = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
# Initialize mss
bounding_box = {'top': 0, 'left': 0, 'width': screensize[0], 'height': screensize[1]}
sct = mss()

prev_background_colour = None
prev_dino_colour = None

x1 = int(input("x1: "))
x2 = int(input("x2: "))
x3 = int(input("x3: "))
y1 = int(input("y1: "))
y2 = int(input("y2: "))
y3 = int(input("y3: "))

def process_img_data(img):
    global prev_background_colour, prev_dino_colour
    global x1, x2, x3, y1, y2, y3
    # Background Colour
    background_colour = list(img[0][0])

    if background_colour != prev_background_colour:
        prev_background_colour = background_colour[::]
        # Get dino colour
        colours = []
        for i in range(0, 600):
            colour = list(img[i][x1])
            if colour != background_colour and colour != [0, 0, 0]:
                colours.append(f"{colour[0]}r{colour[1]}g{colour[2]}b")
        most_common = Counter(colours).most_common()[0][0]
        dino_colour = [int(most_common.split("r")[0]), int(most_common.split("g")[0].split("r")[1]), int(most_common.split("g")[1].split("b")[0])]
        prev_dino_colour = dino_colour[::]
    else:
        dino_colour = prev_dino_colour[::]

    cont = True
    # Find cactuses
    for i in range(x2, x3):
        colour = list(img[y2][i])
        if colour[0] in range(dino_colour[0] - 10, dino_colour[0] + 10) \
            and colour[1] in range(dino_colour[1] - 10, dino_colour[1] + 10) \
                and colour[2] in range(dino_colour[2] - 10, dino_colour[2] + 10):
            pog.press("space")
            cont = False
            break
    
    # Find birds
    if cont:
        for i in range(x2+53, x3+53):
            colour = list(img[y3][i])
            if colour[0] in range(dino_colour[0] - 10, dino_colour[0] + 10) \
                and colour[1] in range(dino_colour[1] - 10, dino_colour[1] + 10) \
                    and colour[2] in range(dino_colour[2] - 10, dino_colour[2] + 10):
                pog.press("space")
                break

time.sleep(5)
while True:
    # Grab Image
    sct_img = sct.grab(bounding_box) 
    # Convert to numpy array
    np_img = np.array(sct_img)
    # Flip colours from BGR to RGB
    np_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB)
    # Convert to Pillow Image
    img = Image.fromarray(np.uint8(np_img))
    # Resize image to 800x600 pixels
    img = img.resize((800, 600))
    # Convert back to numpy array
    np_img = np.array(img)
    # Process image data
    process_img_data(np_img)
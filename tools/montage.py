from imutils import build_montages
from os import listdir
import cv2
import random

faces = [cv2.imread("../outputs/found/" + x) for x in listdir("../outputs/found")]

random.shuffle(faces)

montages = build_montages(faces, (128, 128), (5, 5))

for i, mont in enumerate(montages):
    cv2.imwrite(f"../outputs/non_grouped/{i}.jpg", mont)
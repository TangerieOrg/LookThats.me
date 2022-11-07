import cv2
from flask import make_response
from os import listdir
import random
from imutils import build_montages
import math

def make_response_from_image(image):
    retval, buffer = cv2.imencode('.png', image)

    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

def make_response_montage(path):
    files = listdir(path)
    faces = random.sample(files, min(25, len(files)))
    faces = [cv2.imread(path + x) for x in faces]

    size_len = math.ceil(math.sqrt(len(faces[:25])))

    im = build_montages(faces[:25], (128, 128), (size_len, size_len))[0]

    return make_response_from_image(im)
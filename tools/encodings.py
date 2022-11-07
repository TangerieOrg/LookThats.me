from os import listdir
import face_recognition
from tqdm import tqdm
from PIL import Image
import numpy as np

IMAGE_DIR = "../outputs/found/"
ENCODING_DIR = "../outputs/encodings/"

def getFiles():
    return listdir(IMAGE_DIR)

def getExisting():
    return [".".join(x.split(".")[:-1]) for x in listdir(ENCODING_DIR)]

def getUnprocessed():
    ex = getExisting()
    return [x for x in getFiles() if x not in ex]

if __name__ == "__main__":
    files = getUnprocessed()

    pbar = tqdm(total=len(files))

    for file in files:
        img = face_recognition.load_image_file(f"{IMAGE_DIR}{file}")
        encs = face_recognition.face_encodings(img, None, 100, "large")
        for enc in encs:
            np.save(f"{ENCODING_DIR}/{file}.npy", enc)

        pbar.update(1)
        pbar.set_description_str(f"[{len(listdir(ENCODING_DIR))} Faces]")
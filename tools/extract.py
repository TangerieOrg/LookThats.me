from os import listdir
import face_recognition
from tqdm import tqdm
from PIL import Image
import glob
import numpy as np

FACE_DIR = "/home/tangerie/Instagram/messages/inbox/seenbylmaolliveloligarchyqwewas_jvgouisnua/photos/"

ALL_DIR = "/home/tangerie/Instagram/messages/inbox/*/photos/*"

def getFiles():
    # print(glob.glob(ALL_DIR))
    return glob.glob(ALL_DIR)

def scanForFace(file : str):
    image = face_recognition.load_image_file(file)
    locations = face_recognition.face_locations(image, 1, "cnn")
    return image, locations

def extractFaces(image, scans):
    # print(f"Found {len(scans)} faces")
    images = []
    for scan in scans:
        top, right, bottom, left = scan
        cropped = image[top:bottom, left:right]
        pil_image = Image.fromarray(cropped)
        images.append(pil_image)
    
    return images

def getFilename(path):
    return path.split("/")[-3] + "." + path.split("/")[-1].split(".")[-2]

if __name__ == "__main__":
    with open("log.txt", "r+") as fp:
        log = fp.readlines()

    f = open("log.txt", "a+")
    files = [x for x in getFiles() if x + "\n" not in log]

    pbar = tqdm(total=len(files))

    for file in files:
        image, scan = scanForFace(file)
        encs = face_recognition.face_encodings(image, scan)
        if len(scan) > 0:
            filename = getFilename(file)
            # print(filename)
            for j, image in enumerate(extractFaces(image, scan)):
                with open(f"../outputs/new_found/{filename}.{j}.jpg", "w+") as fp:
                    image.save(fp, "jpeg")
                
                if len(encs) > j:
                    np.save(f"../outputs/new_encs/{filename}.{j}.npy", encs[j])

        f.write(file + "\n")
        pbar.update(1)
        pbar.set_description_str(f"[{len(listdir('../outputs/new_found/'))} | {len(listdir('../outputs/new_encs/'))}]")

    f.close()

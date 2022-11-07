import os
import face_recognition
from tqdm import tqdm
import glob
import numpy as np
import json

# https://github.com/ageitgey/face_recognition

FACE_DIR = "../inputs"
PHOTO_GLOB = f"{FACE_DIR}/*/photos/*"
VIDEO_GLOB = f"{FACE_DIR}/*/videos/*"
MEDIA_GLOB = f"../media/*/*/*"
JSON_FACES_GLOB = "../json/*/*.json"

FilenameParts = tuple[str, str, str, str]
ImageType = np.ndarray

def getNameParts(fullName : str) -> FilenameParts:
    parts = fullName.split("/")
    absName = os.path.abspath(fullName)
    grpFolder = parts[-3]
    grpName = "_".join(grpFolder.split("_")[:-1])
    imgName =  parts[-1]
    return absName, grpName, grpFolder, imgName

def getMediaNameParts(fullName : str) -> FilenameParts:
    parts = fullName.split("/")
    absName = os.path.abspath(fullName)
    grpFolder = parts[-3]
    grpName = "_".join(grpFolder.split("_")[:-1])
    imgName = parts[-2] + "." +  parts[-1]
    return absName, grpName, grpFolder, imgName

def getAllImages():
    return [getNameParts(x) for x in glob.glob(PHOTO_GLOB)]

def getJsonImagesWithFaces():
    return glob.glob(JSON_FACES_GLOB)

def getAllMedia():
    return [getNameParts(x) for x in glob.glob(VIDEO_GLOB)]

def getAllMediaImages():
    return [getMediaNameParts(x) for x in glob.glob(MEDIA_GLOB)]

def chunks(xs, n):
    n = max(1, n)
    return (xs[i:i+n] for i in range(0, len(xs), n))

def getLandmarks(data):
    locations = tuple(tuple(x["location"]) for x in data["results"])
    image = face_recognition.load_image_file(data["filename"])
    landmarks = face_recognition.face_landmarks(image, locations)
    return landmarks

def scanFilesGen(parts: list[FilenameParts]):
    pbar = tqdm(total=len(parts))
    faces_found = 0
    images_scanned = 0
    pbar.set_description_str(f"[{faces_found} Faces | 0 Faces/Image]")
    for fullName, grpName, grpFolder, imgName in parts:
        image = face_recognition.load_image_file(fullName)
        locations = face_recognition.face_locations(image, 1, "cnn")

        faces_found += len(locations)
        images_scanned += 1
        pbar.set_description_str(f"[{faces_found} | {faces_found / images_scanned} Faces/Image]")
        pbar.update(1)

        encodings = face_recognition.face_encodings(image, locations, 1, "large")
        landmarks = face_recognition.face_landmarks(image, locations)

        data = dict(
            filename = fullName,
            groupName = grpName,
            groupFolder = grpFolder,
            imageName = imgName,
            results = []
        )

        for i in range(len(locations)):
            data["results"].append({
                "location": locations[i],
                "encoding": encodings[i].tolist(),
                "landmarks": landmarks[i]
            })

        
        yield data
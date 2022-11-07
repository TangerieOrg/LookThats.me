import json
import glob
import random
import os

# faces.extend([{
#     **result,
#     "filename": randJson["filename"],
#     "groupName": randJson["groupName"],
#     "groupFolder": randJson["groupFolder"],
#     "imageName": randJson["imageName"]
# } for result in randJson["results"]])

def load_num_faces(availableDirs=None, n = 25, load_images=True):
    faces = []
    dir_cache = {}

    if availableDirs is None or availableDirs[0] is None: availableDirs = os.listdir("../json")

    searchedFiles = 0

    while len(faces) < n and len(availableDirs) > 0:
        curDir = random.choice(availableDirs)
        if dir_cache.get(curDir) is None: dir_cache[curDir] = os.listdir(f"../json/{curDir}")

        availableFiles = dir_cache.get(curDir)

        if len(availableFiles) == 0:
            availableDirs.remove(curDir)
            continue

        chosenFile = random.choice(availableFiles)
        availableFiles.remove(chosenFile)

        searchedFiles += 1

        data = load_data_from_file(f"../json/{curDir}/{chosenFile}")
        if len(data["results"]) == 0:
            continue
        


        faces.extend([{
            **result,
            "filename": data["filename"],
            "groupName": data["groupName"],
            "groupFolder": data["groupFolder"],
            "imageName": data["imageName"]
        } for result in data["results"]])

    faces = faces[:n]
    print(f"Found {len(faces)} faces across {searchedFiles} files")

    return faces

# def format_face_results():
    

def load_data_from_file(path):
    with open(path, "r") as fp:
        return json.load(fp)
import json
from util import getJsonImagesWithFaces, getLandmarks
import os
from tqdm import tqdm

for jsonPath in tqdm(getJsonImagesWithFaces()):
    with open(jsonPath, "r") as fp:
        data = json.load(fp)
    landmarks = getLandmarks(data)
    for i in range(len(landmarks)):
        data["results"][i]["landmarks"] = landmarks

    with open(jsonPath, "w") as fp:
        json.dump(data, fp, indent=2)
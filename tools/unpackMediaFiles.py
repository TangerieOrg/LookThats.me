from util import getAllMedia
import cv2
import os
from tqdm import tqdm
import imagehash
from PIL import Image
import glob
import numpy as np

mediaFiles = getAllMedia()

print("Unpacking Media")
for i, file in enumerate(mediaFiles):
    filename, grpName, grpFolder, mediaName = file

    folderPath = f"../media/{grpFolder}/{mediaName}"

    if os.path.exists(folderPath):
        continue

    os.makedirs(folderPath, exist_ok=True)
    vidcap = cv2.VideoCapture(filename)
    numFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"[{i + 1}/{len(mediaFiles)}] Reading {numFrames} from {grpName}/{mediaName}")
    for count in tqdm(range(numFrames)):
        success, image = vidcap.read()
        cv2.imwrite(f"{folderPath}/{count}.jpg", image)


def alpharemover(image):
    if image.mode != 'RGBA':
        return image
    canvas = Image.new('RGBA', image.size, (255, 255, 255, 255))
    canvas.paste(image, mask=image)
    return canvas.convert('RGB')


def with_ztransform_preprocess(hashfunc, hash_size=8):
    def function(path):
        image = alpharemover(Image.open(path))
        image = image.convert("L").resize(
            (hash_size, hash_size), Image.Resampling.LANCZOS)
        data = image.getdata()
        quantiles = np.arange(100)
        quantiles_values = np.percentile(data, quantiles)
        zdata = (np.interp(data, quantiles_values, quantiles) /
                 100 * 255).astype(np.uint8)
        image.putdata(zdata)
        return hashfunc(image)
    return function

dhash_z_transformed = with_ztransform_preprocess(imagehash.dhash, hash_size = 8)


print("Removing Duplicates")
MEDIA_IMAGE_FOLDERS = glob.glob("../media/*/*")

numRemoved = 0
totalLeft = len(glob.glob("../media/*/*/*.jpg"))

pbar = tqdm(total=totalLeft)

for mIndex in range(len(MEDIA_IMAGE_FOLDERS)):
    folder = MEDIA_IMAGE_FOLDERS[mIndex]
    numFiles = len(glob.glob(f"{folder}/*.jpg"))
    # print(f"[{mIndex + 1}/{len(MEDIA_IMAGE_FOLDERS)}] Reading {numFiles} from {folder}")
    filesToCheck = [f"{folder}/{i}.jpg" for i in range(numFiles) if os.path.exists(f"{folder}/{i}.jpg")]
    # hashes = [imagehash.phash(Image.open(x)) for x in filesToCheck]

    refHash = imagehash.phash(Image.open(filesToCheck[0]))
    for i in range(1, len(filesToCheck)):
        curHash = imagehash.phash(Image.open(filesToCheck[i]))
        if refHash - curHash < 60:
            os.remove(filesToCheck[i])
            numRemoved += 1
        else:
            refHash = curHash
        pbar.set_description_str(f"[{numRemoved} | {totalLeft - numRemoved}]")
        pbar.update(1)


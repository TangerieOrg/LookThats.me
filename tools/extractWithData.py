import json
from util import getAllImages, getAllMediaImages, scanFilesGen
import os
import random

filenames = [*getAllImages(), *getAllMediaImages()]

filenames = [x for x in filenames if not os.path.exists(f"../json/{x[2]}/{x[-1]}.json")]

random.shuffle(filenames)

print(f"=== Scanning {len(filenames)} ===")

for data in scanFilesGen(filenames):
    folderPath = f"../json/{data['groupFolder']}"
    os.makedirs(folderPath, exist_ok=True)
    with open(f"{folderPath}/{data['imageName']}.json", "w+") as fp:
        json.dump(data, fp, indent=2)

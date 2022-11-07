from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np
import cv2
from os import listdir, makedirs

def loadEncodings():
    files = listdir("../outputs/encodings/")
    encodings = []
    images = []
    for file in files:
        encodings.append(
            np.load(f"../outputs/encodings/{file}")
        )
        images.append(cv2.imread(f"../outputs/found/{file[:-4]}.jpg"))
    print(f"Loaded {len(encodings)} encodings")
    return images, encodings


images, encodings = loadEncodings()

print("Clustering")
clt = DBSCAN(metric="euclidean", leaf_size=50, n_jobs=4, algorithm='ball_tree')
clt.fit(encodings)

labelIDs = np.unique(clt.labels_)
numUniqueFaces = len(np.where(labelIDs > -1)[0])
print("[INFO] # unique faces: {}".format(numUniqueFaces))

# loop over the unique face integers
for labelID in labelIDs:
    # find all indexes into the `data` array that belong to the
    # current label ID, then randomly sample a maximum of 25 indexes
    # from the set
    clusterFolder = f"../outputs/all_clusters/{labelID}/"
    montageFolder = f"../outputs/montages/{labelID}/"
    
    makedirs(clusterFolder, exist_ok=True)
    makedirs(montageFolder, exist_ok=True)

    # print("[INFO] faces for face ID: {}".format(labelID))
    idxs = np.where(clt.labels_ == labelID)[0]

    all_ims = [images[x] for x in idxs]

    for i, im in enumerate(all_ims):
        print(i)
        cv2.imwrite(f"{clusterFolder}{i}.jpg", im)

    montages = build_montages(all_ims, (256, 256), (5, 5))
    for i, mont in enumerate(montages):
        cv2.imwrite(f"{montageFolder}{i}.jpg", mont)
    # print(idxs)
    # for i in idxs:
    #     print(paths[i])

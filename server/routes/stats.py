from flask import Blueprint
import json, glob

stats_route = Blueprint('stats_route', __name__, url_prefix="/stats")

@stats_route.route("/", methods=['GET'])
def get_stats():
    jsonFiles = glob.glob("../json/*/*.json")
    numFaces = get_num_faces(jsonFiles)

    stats = dict(
        scanned=len(jsonFiles),
        faces=numFaces,
        facesPerImage=numFaces/len(jsonFiles)
    )

    return stats

prev_num_faces = None

def get_num_faces(jsonFiles):
    global prev_num_faces
    if prev_num_faces: return prev_num_faces
    numFaces = 0
    
    for file in jsonFiles:
        with open(file, "r") as fp:
            data = json.load(fp)
            numFaces += len(data["results"])

    prev_num_faces = numFaces

    return numFaces
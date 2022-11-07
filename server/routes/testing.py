from flask import Blueprint, request
import random, json, cv2, glob

from util.images import make_response_from_image

test_route = Blueprint('test_route', __name__, url_prefix="/test")

@test_route.route("/face", methods=['GET'])
def random_face():
    folderPath = request.args.get('folder', '*')
    imagePath = request.args.get('image', '*')
    if request.headers.get('X-Real-IP') != "192.168.0.1": folderPath = "seenbylmaolliveloligarchyqwewas_jvgouisnua"

    jsonGlob = f"../json/{folderPath}/{imagePath}.json"
    jsonPath = random.choice(glob.glob(jsonGlob))
    with open(jsonPath, "r") as fp:
        data = json.load(fp)

    while len(data["results"]) == 0:
        jsonGlob = f"../json/{folderPath}/{imagePath}.json"
        jsonPath = random.choice(glob.glob(jsonGlob))
        with open(jsonPath, "r") as fp:
            data = json.load(fp)

    image = cv2.imread(data["filename"])

    if request.args.get('clear') != "":
        for result in data["results"]:
            location = result["location"]
            top, right, bottom, left = location
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

    res = make_response_from_image(image)

    res.headers.set('X-Image', data["groupFolder"] + "-" + data["imageName"])

    return res

@test_route.route("/frame", methods=['GET'])
def random_frame():
    fileGlob = "../media/*/*/*.jpg"
    img = random.choice(glob.glob(fileGlob))
    return make_response_from_image(cv2.imread(img))
from os import listdir
import random
from flask import Blueprint, request
import json
import glob

from util.format import tryAsIntOr
from util.data import load_num_faces
from util.images import make_response_montage

images_route = Blueprint('images_route', __name__)

@images_route.route("/montage", methods=['GET'])
def montage():
    return make_response_montage("../outputs/found/")

@images_route.route("/montagejson", methods=['GET'])
def montage_from_json():
    folderPath = request.args.get('folder', None)
    if request.headers.get('X-Real-IP') != "192.168.0.1": folderPath = "seenbylmaolliveloligarchyqwewas_jvgouisnua"

    montage_size = tryAsIntOr(request.args.get('size', '5'), 5)

    num_faces = min(montage_size**2, 100)
    print(num_faces)

    return load_num_faces(availableDirs=[folderPath], n=num_faces)

@images_route.route("/similar", methods=['GET'])
def similar():
    selectedDir = random.choice(listdir("../outputs/clusters"))

    return make_response_montage(f"../outputs/clusters/{selectedDir}/")
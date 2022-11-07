from flask import Blueprint, send_from_directory
import os

react_route = Blueprint('react_route', __name__, static_folder=os.path.abspath('../lookthatsme/build'))

# Serve React App
@react_route.route('/', defaults={'path': ''})
@react_route.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(react_route.static_folder + '/' + path):
        return send_from_directory(react_route.static_folder, path)
    else:
        return send_from_directory(react_route.static_folder, 'index.html')
from flask import Flask
from flask_cors import CORS

from util.log import LoggingMiddlware

from routes.images import images_route
from routes.testing import test_route
from routes.react import react_route
from routes.stats import stats_route

app = Flask(__name__, static_folder=react_route.static_folder)
CORS(app)

app.wsgi_app = LoggingMiddlware(app.wsgi_app)

app.register_blueprint(images_route)
app.register_blueprint(test_route)
app.register_blueprint(react_route)
app.register_blueprint(stats_route)

if __name__ == '__main__':
    app.run(debug=True, port=5123, host='0.0.0.0')

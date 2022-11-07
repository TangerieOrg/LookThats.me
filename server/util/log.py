from time import localtime, strftime
from werkzeug.wrappers import Request, Response, ResponseStream


def log(message):
    with open(f"requests.log", "a+") as logfile:
        logfile.write(f"[{strftime('%Y %H:%M:%S', localtime())}] {message}\n")


class LoggingMiddlware():
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        if request.headers.get('X-Real-IP') != "192.168.0.1":
            log(f"{request.path}: {request.headers.get('X-Real-IP')}")

        return self.app(environ, start_response)

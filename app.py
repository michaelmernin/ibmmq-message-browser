import yaml
from flask import Flask
from waitress import serve

import view
from mq_manager import QueueManager
from request_handler import QueueNames

# import sys
# import os


with open("static\ibmmq_configuration.yml") as file:
    QueueManager.conn_details = yaml.load(file, Loader=yaml.FullLoader)

app = Flask(__name__)

app.register_blueprint(view.view)

# When using Pyinstaller
# if getattr(sys, 'frozen', False):
#     template_folder = os.path.join(sys._MEIPASS, 'templates')
#     static_folder = os.path.join(sys._MEIPASS, 'static')
#     app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
# else:
#     app = Flask(__name__)


if __name__ == '__main__':
    app.debug = True
    app.config["JSON_SORT_KEYS"] = False
    app.config['DEFAULT_PARSERS'] = [
        'flask.ext.api.parsers.JSONParser',
        'flask.ext.api.parsers.URLEncodedParser',
        'flask.ext.api.parsers.MultiPartParser'
    ]
    # Product WSGI server "waitress"
    # serve(app, host='127.0.0.1', port='5000')
    # serve(app, host='0.0.0.0', port='5000')

    # Flask built in server
    app.run()

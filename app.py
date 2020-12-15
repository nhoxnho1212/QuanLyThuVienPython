from flask import render_template

from server import create_app
from DevelopmentConfig import config
from flask_cors import CORS

app = create_app(config)
CORS(app)

if __name__ == '__main__':
    app.run()

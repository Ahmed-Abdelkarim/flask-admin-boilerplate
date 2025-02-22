from flask import Flask
app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev' )
from views import *

if __name__ == "__main__":
    app.run(debug="true")
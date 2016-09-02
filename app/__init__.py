from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__)
app.config.from_object('config')
CORS(app)

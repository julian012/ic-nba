from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

from app import views, models
from app.db import db

db.create_all()

from flask import Flask


app = Flask(__name__)

from app import views, models
from app.db import db

db.create_all()

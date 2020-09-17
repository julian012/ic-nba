from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

HOST = 'ec2-35-172-73-125.compute-1.amazonaws.com'
DATABASE = 'dbhbu2mce42c2h'
USER = 'lpbokbiofopknm'
PASSWORD = '94efb703ce2d583eb7eac19d8e35f9ef304d45de091345a6061f77f5a133a1cd'


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://zmvsxfgv:IIq9KxS2JnoLFsEAAB8z7nB4_adR_SXb@lallah.db.elephantsql.com:5432/zmvsxfgv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
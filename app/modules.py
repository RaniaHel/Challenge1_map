from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/challenge1.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class States(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), unique=True)
    annual_net = db.Column(db.String(100))
    annual_net_percentage = db.Column(db.String(100))
    lat = db.Column(db.String(100))
    lon = db.Column(db.String(100))


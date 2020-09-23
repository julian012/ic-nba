from app.db import db


class TeamMatchResultPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(100))
    home_team = db.Column(db.String(100))
    prediction_home_team = db.Column(db.Float)
    away_team = db.Column(db.String(100))
    prediction_away_team = db.Column(db.Float)

    def __init__(self, date, home_team, prediction_home_team, away_team, prediction_away_team):
        self.date = date
        self.home_team = home_team
        self.prediction_home_team = prediction_home_team
        self.away_team = away_team
        self.prediction_away_team = prediction_away_team
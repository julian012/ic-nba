from app.db import db


class TeamBoxScore(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assists = db.Column(db.Integer)
    attempted_field_goals = db.Column(db.Integer)
    attempted_free_throws = db.Column(db.Integer)
    attempted_three_point_field_goals = db.Column(db.Integer)
    blocks = db.Column(db.String(100))
    date = db.Column(db.String(100), primary_key=True)
    defensive_rebounds = db.Column(db.Integer)
    made_field_goals = db.Column(db.Integer)
    made_free_throws = db.Column(db.Integer)
    made_three_point_field_goals = db.Column(db.String(100))
    minutes_played = db.Column(db.String(100))
    offensive_rebounds = db.Column(db.Integer)
    outcome = db.Column(db.String(100))
    personal_fouls = db.Column(db.Integer)
    points = db.Column(db.Integer)
    steals = db.Column(db.Integer)
    team = db.Column(db.String(100), primary_key=True)
    turnovers = db.Column(db.Integer)

    def __init__(self, assists, attempted_field_goals, attempted_free_throws, attempted_three_point_field_goals,
                 blocks, date, defensive_rebounds, made_field_goals, made_free_throws, made_three_point_field_goals,
                 minutes_played, offensive_rebounds, outcome, personal_fouls, points, steals, team, turnovers):
        self.assists = assists
        self.attempted_field_goals = attempted_field_goals
        self.attempted_free_throws = attempted_free_throws
        self.attempted_three_point_field_goals = attempted_three_point_field_goals
        self.blocks = blocks
        self.date = date
        self.defensive_rebounds = defensive_rebounds
        self.made_field_goals = made_field_goals
        self.made_free_throws = made_free_throws
        self.made_three_point_field_goals = made_three_point_field_goals
        self.minutes_played = minutes_played
        self.offensive_rebounds = offensive_rebounds
        self.outcome = outcome
        self.personal_fouls = personal_fouls
        self.points = points
        self.steals = steals
        self.team = team
        self.turnovers = turnovers

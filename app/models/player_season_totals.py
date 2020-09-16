from app.db import db


class PlayerSeasonTotals(db.Model):

    age = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    attempted_field_goals = db.Column(db.Integer)
    attempted_free_throws = db.Column(db.Integer)
    attempted_three_point_field_goals = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    defensive_rebounds = db.Column(db.Integer)
    games_played = db.Column(db.Integer)
    games_started = db.Column(db.Integer)
    made_field_goals = db.Column(db.Integer)
    made_free_throws = db.Column(db.Integer)
    made_three_point_field_goals = db.Column(db.Integer)
    minutes_played = db.Column(db.Integer)
    name = db.Column(db.String(100))
    offensive_rebounds = db.Column(db.Integer)
    personal_fouls = db.Column(db.Integer)
    points = db.Column(db.Integer)
    positions = db.Column(db.ARRAY(db.String))
    slug = db.Column(db.String(100), primary_key=True)
    steals = db.Column(db.Integer)
    team = db.Column(db.String(100), primary_key=True)
    turnovers = db.Column(db.Integer)

    def __init__(self, age, assists, attempted_field_goals, attempted_free_throws, attempted_three_point_field_goals,
                 blocks, defensive_rebounds, games_played, games_started, made_field_goals, made_free_throws,
                 made_three_point_field_goals, minutes_played, name, offensive_rebounds, personal_fouls, points,
                 positions, slug, steals, team, turnovers):
        self.age = age
        self.assists = assists
        self.attempted_field_goals = attempted_field_goals
        self.attempted_free_throws = attempted_free_throws
        self.attempted_three_point_field_goals = attempted_three_point_field_goals
        self.blocks = blocks
        self.defensive_rebounds = defensive_rebounds
        self.games_played = games_played
        self.games_started = games_started
        self.made_field_goals = made_field_goals
        self.made_free_throws = made_free_throws
        self.made_three_point_field_goals = made_three_point_field_goals
        self.minutes_played = minutes_played
        self.name = name
        self.offensive_rebounds = offensive_rebounds
        self.personal_fouls = personal_fouls
        self.points = points
        self.positions = positions
        self.slug = slug
        self.steals = steals
        self.team = team
        self.turnovers = turnovers

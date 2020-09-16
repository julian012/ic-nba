from app.db import db


class PlayerBoxScore(db.Model):
    
    assists = db.Column(db.Integer)
    attempted_field_goals = db.Column(db.Integer)
    attempted_free_throws = db.Column(db.Integer)
    attempted_three_point_field_goals = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    date = db.Column(db.String(100), primary_key=True)
    defensive_rebounds = db.Column(db.Integer)
    game_score = db.Column(db.Integer)
    location = db.Column(db.String(100))
    made_field_goals = db.Column(db.Integer)
    made_free_throws = db.Column(db.Integer)
    made_three_point_field_goals = db.Column(db.Integer)
    offensive_rebounds = db.Column(db.Integer)
    opponent = db.Column(db.String(100))
    outcome = db.Column(db.String(100))
    personal_fouls = db.Column(db.Integer)
    plus_minus = db.Column(db.Integer)
    points_scored = db.Column(db.Integer)
    seconds_played = db.Column(db.Integer)
    steals = db.Column(db.Integer)
    slug = db.Column(db.String(100), primary_key=True)
    team = db.Column(db.String(100))
    turnovers = db.Column(db.Integer)

    def __init__(self, assists, attempted_field_goals, attempted_free_throws, attempted_three_point_field_goals,
                 blocks, date, defensive_rebounds, game_score, location, made_field_goals, made_free_throws,
                 made_three_point_field_goals, offensive_rebounds, opponent, outcome, personal_fouls, plus_minus,
                 points_scored, seconds_played, steals, slug, team, turnovers):
        self.assists = assists
        self.attempted_field_goals = attempted_field_goals
        self.attempted_free_throws = attempted_free_throws
        self.attempted_three_point_field_goals = attempted_three_point_field_goals
        self.blocks = blocks
        self.date = date
        self.defensive_rebounds = defensive_rebounds
        self.game_score = game_score
        self.location = location
        self.made_field_goals = made_field_goals
        self.made_free_throws = made_free_throws
        self.made_three_point_field_goals = made_three_point_field_goals
        self.offensive_rebounds = offensive_rebounds
        self.opponent = opponent
        self.outcome = outcome
        self.personal_fouls = personal_fouls
        self.plus_minus = plus_minus
        self.points_scored = points_scored
        self.seconds_played = seconds_played
        self.steals = steals
        self.slug = slug
        self.team = team
        self.turnovers = turnovers
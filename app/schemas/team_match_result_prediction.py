from app.db import ma


class TeamMatchResultPredictionSchema(ma.Schema):
    class Meta:
        fields = ('date', 'home_team', 'prediction_home_team', 'away_team', 'prediction_away_team')


team_match_result_prediction_schema = TeamMatchResultPredictionSchema()
teams_match_result_prediction_schema = TeamMatchResultPredictionSchema(many=True)
from app.db import ma


class TeamBoxScoreSchema(ma.Schema):
    class Meta:
        fields = ('assists', 'attempted_field_goals', 'attempted_free_throws', 'attempted_three_point_field_goals',
                  'blocks', 'date', 'defensive_rebounds', 'made_field_goals', 'made_free_throws',
                  'made_three_point_field_goals', 'minutes_played', 'offensive_rebounds', 'outcome', 'personal_fouls',
                  'points', 'steals', 'team', 'turnovers')


team_box_score_schema = TeamBoxScoreSchema()
teams_box_score_schema = TeamBoxScoreSchema(many=True)

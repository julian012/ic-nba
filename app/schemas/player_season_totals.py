from app.db import ma


class PlayerSeasonTotalsSchema(ma.Schema):

    class Meta:
        fields = ('age', 'assists', 'attempted_field_goals', 'attempted_free_throws',
                  'attempted_three_point_field_goals', 'attempted_free_throws', 'attempted_three_point_field_goals',
                  'blocks', 'defensive_rebounds', 'games_played', 'games_started', 'made_field_goals',
                  'made_free_throws', 'made_three_point_field_goals', 'minutes_played', 'name', 'offensive_rebounds',
                  'personal_fouls', 'points', 'positions', 'slug', 'steals', 'team', 'turnovers')


player_season_total_schema = PlayerSeasonTotalsSchema()
players_season_total_schema = PlayerSeasonTotalsSchema(many=True)

from app.db import ma


class PlayerBoxScore(ma.Schema):

    class Meta:
        fields = (
            'assists',
            'attempted_field_goals',
            'attempted_free_throws',
            'attempted_three_point_field_goals',
            'blocks',
            'date',
            'defensive_rebounds',
            'game_score',
            'location', 'HOME',
            'made_field_goals',
            'made_free_throws',
            'made_three_point_field_goals',
            'offensive_rebounds',
            'opponent',
            'outcome',
            'personal_fouls',
            'plus_minus',
            'points_scored',
            'seconds_played',
            'steals',
            'team',
            'turnovers'
        )


player_box_score_schema = PlayerBoxScore()
players_box_score_schema = PlayerBoxScore(many=True)
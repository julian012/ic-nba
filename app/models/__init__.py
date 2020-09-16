from app.models.player_season_totals import PlayerSeasonTotals
from app.models.player_box_score import PlayerBoxScore
from app.models.team_box_score import TeamBoxScore


def create_team_box_score(team, date):
    return TeamBoxScore(
        team['assists'],
        team['attempted_field_goals'],
        team['attempted_free_throws'],
        team['attempted_three_point_field_goals'],
        team['blocks'],
        date,
        team['defensive_rebounds'],
        team['made_field_goals'],
        team['made_free_throws'],
        team['made_three_point_field_goals'],
        team['minutes_played'],
        team['offensive_rebounds'],
        team['outcome'],
        team['personal_fouls'],
        team['points'],
        team['steals'],
        team['team'],
        team['turnovers']
    )


def create_player_season_total(player):
    return PlayerSeasonTotals(
        player['age'],
        player['assists'],
        player['attempted_field_goals'],
        player['attempted_free_throws'],
        player['attempted_three_point_field_goals'],
        player['blocks'],
        player['defensive_rebounds'],
        player['games_played'],
        player['games_started'],
        player['made_field_goals'],
        player['made_free_throws'],
        player['made_three_point_field_goals'],
        player['minutes_played'],
        player['name'],
        player['offensive_rebounds'],
        player['personal_fouls'],
        player['points'],
        player['positions'],
        player['slug'],
        player['steals'],
        player['team'],
        player['turnovers']
    )


def create_player_box_score(player, slug):
    return PlayerBoxScore(
        player['assists'],
        player['attempted_field_goals'],
        player['attempted_free_throws'],
        player['attempted_three_point_field_goals'],
        player['blocks'],
        player['date'],
        player['defensive_rebounds'],
        player['game_score'],
        player['location'],
        player['made_field_goals'],
        player['made_free_throws'],
        player['made_three_point_field_goals'],
        player['offensive_rebounds'],
        player['opponent'],
        player['outcome'],
        player['personal_fouls'],
        player['plus_minus'],
        player['points_scored'],
        player['seconds_played'],
        player['steals'],
        slug,
        player['team'],
        player['turnovers']
    )

# getStats.py - Obtains a grouping of stats for any team in the NBA

from .config.teamIds import teams
from nba_api.stats.endpoints import teamdashboardbygeneralsplits
import time
from .config.customHeaders import customHeaders


# Returns various stats for inputted team in a dictionary
# team should match team name in teamIds.py
# startDate and endDate should be in format 'mm/dd/yyyy'
def get_stats_for_team(team, start_date, end_date, season='2019-20'):
    time.sleep(1)
    # Uses NBA_API to access the dictionary holding basic stats for every team per 100 possessions
    general_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
        team_id=teams[team],
        per_mode_detailed='Per100Possessions',
        date_from_nullable=start_date,
        date_to_nullable=end_date,
        season=season,
        headers=customHeaders,
        timeout=3000
    )
    general_team_dict = general_team_info.get_normalized_dict()
    general_team_dashboard = general_team_dict['OverallTeamDashboard'][0]

    # Returns Win PCT, Rebounds, Turnovers, and Plus Minus
    win_percentage = general_team_dashboard['W_PCT']
    rebounds = general_team_dashboard['REB']
    turnovers = general_team_dashboard['TOV']
    plus_minus = general_team_dashboard['PLUS_MINUS']

    # Uses NBA_API to access the dictionary holding advanced stats for every team
    advanced_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
        team_id=teams[team],
        measure_type_detailed_defense='Advanced',
        date_from_nullable=start_date,
        date_to_nullable=end_date,
        season=season,
        headers=customHeaders,
        timeout=3000
    )

    advanced_team_dict = advanced_team_info.get_normalized_dict()
    advanced_team_dashboard = advanced_team_dict['OverallTeamDashboard'][0]

    # Variables holding OFF Rating, DEF Rating, and TS%
    offensive_rating = advanced_team_dashboard['OFF_RATING']
    defensive_rating = advanced_team_dashboard['DEF_RATING']
    true_shooting_percentage = advanced_team_dashboard['TS_PCT']

    # Puts all the stats for specified team into a dictionary
    return {
        'W_PCT': win_percentage,
        'REB': rebounds,
        'TOV': turnovers,
        'PLUS_MINUS': plus_minus,
        'OFF_RATING': offensive_rating,
        'DEF_RATING': defensive_rating,
        'TS_PCT': true_shooting_percentage,
    }

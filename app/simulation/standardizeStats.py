# standardizeStats.py - Uses Z Scores ((Obs  - Mean) / St Dev.) to standardize any of the different statistics scraped

from nba_api.stats.endpoints import leaguedashteamstats
import statistics
import time
from .config.customHeaders import customHeaders


# Finds league mean for the entered basic or advanced statistic (statType = 'Base' or 'Advanced')
def basic_or_advanced_stat_mean(start_date, end_date, stat, stat_type='Base', season='2018-19'):
    time.sleep(.2)
    # Gets list of dictionaries with stats for every team
    all_teams_info = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions',
                                                             measure_type_detailed_defense=stat_type,
                                                             date_from_nullable=start_date,
                                                             date_to_nullable=end_date,
                                                             season=season,
                                                             headers=customHeaders,
                                                             timeout=300)
    all_teams_dict = all_teams_info.get_normalized_dict()
    all_teams_list = all_teams_dict['LeagueDashTeamStats']
    specific_stat_all_teams = []
    for i in range(len(
            all_teams_list)):  # Loops through and appends specific stat to new list until every team's stat has been added
        specific_stat_all_teams.append(all_teams_list[i][stat])
    mean = statistics.mean(specific_stat_all_teams)  # Finds mean of stat
    return mean


# Finds league standard deviation for the entered basic or advanced statistic (statType = 'Base' or 'Advanced')
def basic_or_advanced_stat_standard_deviation(start_date, end_date, stat, stat_type='Base', season='2018-19'):
    time.sleep(.2)
    # Gets list of dictionaries with stats for every team
    all_teams_info = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions',
                                                             measure_type_detailed_defense=stat_type,
                                                             date_from_nullable=start_date,
                                                             date_to_nullable=end_date,
                                                             season=season,
                                                             headers=customHeaders,
                                                             timeout=120)
    all_teams_dict = all_teams_info.get_normalized_dict()
    all_teams_list = all_teams_dict['LeagueDashTeamStats']
    specific_stat_all_teams = []
    for i in range(
            len(all_teams_list)):  # Loops and appends specific stat to new list until every team's stat has been added
        specific_stat_all_teams.append(all_teams_list[i][stat])
    standard_deviation = statistics.stdev(specific_stat_all_teams)  # Finds standard deviation of stat
    return standard_deviation


# Returns a standardized version of each data point via the z-score method
def basic_or_advanced_stat_z_score(observed_stat, mean, standard_deviation):
    return (observed_stat - mean) / standard_deviation  # Calculation for z-score

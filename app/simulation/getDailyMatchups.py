# getDailyMatchups.py - Finds the daily NBA games

from nba_api.stats.endpoints import scoreboard, leaguegamelog
from .config.teamIds import teams
from .config.customHeaders import customHeaders


# Function to get you the games on a specified date (Home vs. Away)
# Used for dates in the present or future
# Return value is a list where index 0 is a dict holding the games  {Home:Away}
# Enter a date in the format mm/dd/yyyy
def daily_match_ups_present(date):

    # Obtains all games that are set to occur on specified date
    daily_matchups = scoreboard.Scoreboard(
        league_id='00',
        game_date=date,
        headers=customHeaders,
        timeout=3000
    )
    daily_matchups_dict = daily_matchups.get_normalized_dict()
    list_of_games = daily_matchups_dict['GameHeader']

    home_away_dict = {}

    for game in list_of_games:  # Loops through each game on date

        home_team_id = game['HOME_TEAM_ID']

        for team, teamID in teams.items():  # Finds name of the home team that corresponds with teamID
            if teamID == home_team_id:
                home_team_name = team

        away_team_id = game['VISITOR_TEAM_ID']

        for team, teamID in teams.items():  # Finds name of the away team that corresponds with teamID
            if teamID == away_team_id:
                away_team_name = team

        # TODO HACE LOS PARES ENTRE EQUIPO LOCAL Y VISITANTE QUE SE VAN A ENFRENTAR EN DICHA FECHA
        home_away_dict.update({home_team_name: away_team_name})

    return home_away_dict

def dailyMatchupsPast(date, season):

    # Obtains a list of teams who played on specified date
    dailyMatchups = leaguegamelog.LeagueGameLog(
        season=season,
        league_id='00',
        season_type_all_star='Regular Season',
        date_from_nullable=date,date_to_nullable=date,
        headers=customHeaders,
        timeout=3000)
    dailyMatchupsDict = dailyMatchups.get_normalized_dict()
    listOfTeams = dailyMatchupsDict['LeagueGameLog']

    winLossList = []
    homeAwayDict = {}
    for i in range(0,len(listOfTeams),2):  # Loops through every other team
        if '@' in listOfTeams[i]['MATCHUP']:  # @ in matchup indicates that the current team is away
            awayTeam = listOfTeams[i]['TEAM_NAME']
            homeTeam = listOfTeams[i+1]['TEAM_NAME']

            winLossList.append(listOfTeams[i+1]['WL'])  # Appends if the home team won or lost to list

        else:
            awayTeam = listOfTeams[i+1]['TEAM_NAME']
            homeTeam = listOfTeams[i]['TEAM_NAME']

            winLossList.append(listOfTeams[i]['WL'])  # Appends if the home team won or lost to the list

        homeAwayDict.update({homeTeam:awayTeam})  # Adds current game to list of all games for that day

    matchupsResultCombined = [homeAwayDict, winLossList]  # Combines games and win/loss results into one list
    return(matchupsResultCombined)

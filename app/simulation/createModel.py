# createModel.py - Used to train, test, and create the model
# Call createModel() to generate a new model
# May need to edit which lines are commented out based on what range of game data you would like to use

from .standardizeStats import basic_or_advanced_stat_mean, basic_or_advanced_stat_standard_deviation, \
    basic_or_advanced_stat_z_score
from .getDailyMatchups import dailyMatchupsPast
from .getStats import get_stats_for_team
from .config.availableStats import availableStats
from .config.configureCWD import set_current_working_directory

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pandas as pd
import pickle

from datetime import timedelta, date


# Returns a list. Index 0 is a dict holding mean for each stat. Index 1 is a dict holding standard deviation for each
# stat.
def create_mean_standard_deviation_dicts(start_date, end_date, season):

    mean_dict = {}
    standard_deviation_dict = {}

    # Loops through and inputs standard deviation and mean for each stat into dict
    for stat, statType in availableStats.items():
        stat_mean = basic_or_advanced_stat_mean(start_date, end_date, stat, statType, season)
        mean_dict.update({stat: stat_mean})

        stat_standard_deviation = basic_or_advanced_stat_standard_deviation(start_date, end_date, stat, statType, season)
        standard_deviation_dict.update({stat: stat_standard_deviation})

    # TODO OBTIENE LA MEDIA Y LA DESVIACIÓN ESTANDAR DE LAS ESTADISTICAS TOTALES POR EQUIPO
    both_dicts = [mean_dict, standard_deviation_dict]
    return both_dicts


# Calculates the zScore differential between two teams for a specified stat
def z_score_differential(observed_stat_home, observed_stat_away, mean, standard_deviation):

    home_team_z_score = basic_or_advanced_stat_z_score(observed_stat_home, mean, standard_deviation)
    away_team_z_score = basic_or_advanced_stat_z_score(observed_stat_away, mean, standard_deviation)

    return home_team_z_score - away_team_z_score


# Used to combine and format all the data to be put into a pandas dataframe
# dailyGames should be list where index 0 is a dictionary holding the games and index 1 is a list holding the results
def info_to_data_frame(daily_games, mean_dict, standard_deviation_dict, start_date, end_date, season):

    full_data_frame = []
    game_number = 0  # Counter to match the result of the game with the correct game
    daily_results = daily_games[1]  # List of results for the games

    for homeTeam,awayTeam in daily_games[0].items():

        home_team_stats = get_stats_for_team(homeTeam, start_date, end_date, season)
        away_team_stats = get_stats_for_team(awayTeam, start_date, end_date, season)

        current_game = [homeTeam,awayTeam]

        for stat, statType in availableStats.items():  # Finds Z Score Dif for stats listed above and adds them to list
            z_score_dif = z_score_differential(
                home_team_stats[stat],
                away_team_stats[stat],
                mean_dict[stat],
                standard_deviation_dict[stat]
            )
            current_game.append(z_score_dif)

        if daily_results[game_number] == 'W':  # Sets result to 1 if a win
            result = 1
        else:  # Sets result to 0 if loss
            result = 0

        current_game.append(result)
        game_number += 1

        print(current_game)
        full_data_frame.append(current_game)  # Adds this list to list of all games on specified date

    return full_data_frame


# Function that allows iterating through specified start date to end date
def date_range(start_date, end_date):

    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_training_set(start_year, start_month, start_day, end_year, end_month, end_day, season, start_of_season):

    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    startDateFormatted = start_date.strftime("%m/%d/%Y")  # Formats start date in mm/dd/yyyy
    all_games = []

    for singleDate in date_range(start_date, end_date):
        current_date = singleDate.strftime("%m/%d/%Y")  # Formats current date in mm/dd/yyyy
        print(current_date)

        previous_day = singleDate - timedelta(days=1)
        previous_day_formatted = previous_day.strftime("%m/%d/%Y")

        mean_and_standard_deviation_dicts = create_mean_standard_deviation_dicts(start_of_season, previous_day_formatted, season)
        mean_dict = mean_and_standard_deviation_dicts[0]  # Dict in format {stat:statMean}
        standard_deviation_dict = mean_and_standard_deviation_dicts[1]  # Dict in format {stat:statStDev}

        current_day_games = dailyMatchupsPast(current_date, season)  # Finds games on current date in loop
        current_day_games_and_stats_list = info_to_data_frame(current_day_games, mean_dict, standard_deviation_dict, start_of_season, previous_day_formatted, season)  # Formats Z Score difs for games on current date in loop

        for game in current_day_games_and_stats_list:  # Adds game with stats to list of all games
            game.append(current_date)
            all_games.append(game)

    return all_games


# Returns a dataframe from list of games with z score differentials
def create_data_frame(list_of_games):
    games = pd.DataFrame(
        list_of_games,
        columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT', 'Result', 'Date']
    )
    return games


# Creates the logistic regression model and tests accuracy
def perform_log_reg(data_frame):

    # Update if new stats are added
    feature_columns = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

    X = data_frame[feature_columns] # Features
    Y = data_frame.Result  # Target Variable

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, shuffle=True)
    logreg = LogisticRegression()

    logreg.fit(X_train, Y_train)  # Fits model with data

    Y_pred = logreg.predict(X_test)

    confusionMatrix = metrics.confusion_matrix(Y_test, Y_pred)  # Diagonals tell you correct predictions

    # Code below prints model accuracy information
    print('Coefficient Information:')

    for i in range(len(feature_columns)):  # Prints each feature next to its corresponding coefficient in the model

        logregCoefficients = logreg.coef_

        currentFeature = feature_columns[i]
        currentCoefficient = logregCoefficients[0][i]

        print(currentFeature + ': ' + str(currentCoefficient))

    print('----------------------------------')

    print("Accuracy:", metrics.accuracy_score(Y_test, Y_pred))
    print("Precision:", metrics.precision_score(Y_test, Y_pred))
    print("Recall:", metrics.recall_score(Y_test, Y_pred))

    print('----------------------------------')

    print('Confusion Matrix:')
    print(confusionMatrix)

    return logreg


# Saves the model in folder to be used in future
# filename should be end in '.pkl'
def saveModel(model, filename):

    # Change to where you want to save the model
    set_current_working_directory('SavedModels')

    with open(filename, 'wb') as file:
        pickle.dump(model, file)


# Used to generate new logistic regression models
# Can import the statistics and predictions for each game from a csv file or can be created on their own
def createModel(startYear=None, startMonth=None, startDay=None, endYear=None, endMonth=None, endDay=None, season='2018-19', startOfSeason = '10/16/2018', filename='model.pkl'):

    # allGames = getTrainingSet(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startOfSeason)  # Unnecessary if using data from CSV file

    # allGamesDataframe = createDataFrame(allGames)  # Unnecessary if using data from CSV file

    set_current_working_directory('Data')
    allGamesDataframe = pd.read_csv('COMBINEDgamesWithInfo2016-19.csv')  # Should be commented out if needing to obtain data on different range of games

    logRegModel = perform_log_reg(allGamesDataframe)

    saveModel(logRegModel, filename)

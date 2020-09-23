# nbaPredict.py - Predicts results of NBA games on a specified date
# Call makeInterpretPrediction with current date, season, and start date of season to run predictions

import pickle
import pandas as pd

from .getDailyMatchups import daily_match_ups_present
from .createModel import create_mean_standard_deviation_dicts, z_score_differential
from .config.availableStats import availableStats
from .getStats import get_stats_for_team
from .config.configureCWD import set_current_working_directory
from app.models.team_match_result_prediction import TeamMatchResultPrediction


# Obtiene juegos en la fecha establecida y devuelve predicciones para cada juego
# currentDate/startOfSeason should be in form 'mm/dd/yyyy' and season in form 'yyyy-yy'
# Start of 2019-20 season was 10/2/2019
def make_interpret_predictions(current_date, season, start_of_season):
    set_current_working_directory('../SavedModels')
    print('Predictions for ' + current_date + ':')
    predictions = predict_daily_games(current_date, season, start_of_season)
    return interpret_predictions(predictions, current_date)


# Returns a list
# Index 0 is the dailyGames in dict form {Home:Away}
# Index 1 is a list with the prediction probabilities for each game [[lossProb, winProb]]
# currentDate should be in form 'mm/dd/yyyy' and season in form 'yyyy-yy'
def predict_daily_games(current_date, season, start_of_season):
    # TODO Sirven las fechas almacenadas en la base de datos mm/dd/yyyy
    # Obtiene todos los juegos para la fecha especificada
    # TODO --> Resultado {'Equipo local':'Equipo visitante'}
    daily_games = daily_match_ups_present(current_date)
    print('daily_games', daily_games)
    # Media y Desviación estandar
    mean_dict, standard_deviation_dict = create_mean_standard_deviation_dicts(start_of_season, current_date, season)

    daily_games_list = daily_games_data_frame(daily_games, mean_dict, standard_deviation_dict, start_of_season,
                                              current_date, season)

    # Pandas dataframe holding daily games and Z-Score differentials between teams
    # TODO: Tiene los juegos diarios y los z-score entre los equipos
    games_with_z_score_difs = pd.DataFrame(
        daily_games_list,
        columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
    )
    # TODO: Se toman solo los dats que se van a usaer
    just_z_score_difs = games_with_z_score_difs.loc[:, 'W_PCT':'TS_PCT']  # Slices only the features used in the model

    with open('finalized_model.pkl', 'rb') as file:  # Change filename here if model is named differently
        pickle_model = pickle.load(file)

    predictions = pickle_model.predict_proba(just_z_score_difs)  # Predicts the probability that the home team loses/wins
    # TODO: Envida la prediccion de los juegos
    print(predictions)
    games_with_predictions = [daily_games, predictions]
    return games_with_predictions


# Returns list of games with Z-Score differentials between teams to be put into a Pandas dataframe
# startDate & endDate should be 'mm/dd/yyyy' form
# TODO: TENIENDO LA DESVIACION ESTANDAR Y LA MEDIA Y LOS JUEGOS A DISPUTAR REALIZA EL ANALISIS POR ENFRENTAMIENTO
def daily_games_data_frame(daily_games, mean_dict, standard_deviation_dict, start_date, end_date, season):
    full_data_frame = []

    for homeTeam, awayTeam in daily_games.items():

        # TODO SE OBTIENIENEN LAS ESTADISTICAS DEL EQUIPO EN ESE ENCUENTRO, LOCAL COMO VISITANTE
        home_team_stats = get_stats_for_team(homeTeam, start_date, end_date, season)
        away_team_stats = get_stats_for_team(awayTeam, start_date, end_date, season)

        current_game = [homeTeam, awayTeam]

        for stat, statType in availableStats.items():  # Finds Z Score Dif for stats listed above and adds them to list
            # TODO SE CALCULA EL Z-SCORE ENTRE LAS ESTADISTICAS DE LOCAL, VISITANTE, MEDIA, Y DESVIACIÓN
            z_score_dif = z_score_differential(
                home_team_stats[stat],
                away_team_stats[stat],
                mean_dict[stat],
                standard_deviation_dict[stat]
            )
            current_game.append(z_score_dif)

        full_data_frame.append(current_game)  # Adds this list to list of all games on specified date

    return full_data_frame


# Returns the percent chance that the home team will defeat the away team for each game
# gamesWithPredictions should be in form [dailyGames, predictionsList]
def interpret_predictions(games_with_predictions, current_date):
    daily_games = games_with_predictions[0]  # Dict holding daily matchups
    probability_predictions = games_with_predictions[1]  # List of lists holding probs of loss/win for home team
    result = []

    for gameNum in range(len(probability_predictions)):  # Loops through each game

        win_prob = probability_predictions[gameNum][1]
        win_prob_rounded = round(win_prob, 4)
        win_prob_percent = "{:.2%}".format(win_prob_rounded)  # Formulates percent chance that home team wins

        home_team = list(daily_games.keys())[gameNum]
        away_team = list(daily_games.values())[gameNum]

        #print('There is a ' + win_prob_percent + ' chance that the ' + home_team + ' will defeat the ' + away_team + '.')
        #print(home_team, probability_predictions[gameNum][1], away_team, probability_predictions[gameNum][0])

        prediction = TeamMatchResultPrediction(
            current_date,
            home_team,
            probability_predictions[gameNum][1],
            away_team,
            probability_predictions[gameNum][0]
        )
        result.append(prediction)

    return result


# EDIT THIS
# El primer argumento es la fecha para predecir (mm / dd / aaaa), el segundo es la temporada (aaaa-aa) y 
# el tercero es la fecha de inicio de la temporada (mm / dd / aaaa)
# make_interpret_predictions('01/04/2020', '2019-20', '10/22/2019')

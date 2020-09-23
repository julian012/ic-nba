from app import app
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from app.models.player_season_totals import PlayerSeasonTotals
from app.models.player_box_score import PlayerBoxScore
from app.models.team_box_score import TeamBoxScore
from app.schemas.team_box_score import team_box_score_schema, teams_box_score_schema
from app.schemas.player_season_totals import players_season_total_schema
from app.db import db
from app.models import create_player_season_total, create_player_box_score, create_team_box_score
from sqlalchemy import distinct
import json
from flask import jsonify
from datetime import datetime
from app.simulation.nbaPredict import make_interpret_predictions
import numpy as np
import os
import re

current_path = os.path.dirname(__file__)


@app.route('/fill/<year>', methods=['GET'])
def player_season_total(year):
    players = json.loads(client.players_season_totals(season_end_year=year, output_type=OutputType.JSON))

    for player in players:
        new_player = create_player_season_total(player)

        player_boxes = json.loads(
            client.regular_season_player_box_scores(player_identifier=player['slug'], season_end_year=year,
                                                    output_type=OutputType.JSON))
        for player_box in player_boxes:
            new_player_box = create_player_box_score(player_box, player['slug'])
            try:
                db.session.add(new_player_box)
                db.session.commit()
            except:
                db.session.rollback()

        db.session.add(new_player)
        db.session.commit()

    return str(len(players)) + ' Registros de jugadores agregados correctamente'


@app.route('/player/season/total', methods=['DELETE'])
def delete_player_season_total():
    num_rows_deleted = db.session.query(PlayerSeasonTotals).delete()
    db.session.commit()
    db.session.rollback()
    return str(num_rows_deleted) + ' Registos borrados'


@app.route('/fill/team-box')
def fill_team_box_score():
    dates = db.session.query(distinct(PlayerBoxScore.date)).all()
    for date in dates:
        date_time_obj = datetime.strptime(str(date), "('%Y-%m-%d',)")
        date_converted = date_time_obj.strftime('%Y-%m-%d')
        team_box_scores = json.loads(
            client.team_box_scores(day=date_time_obj.day, month=date_time_obj.month, year=date_time_obj.year,
                                   output_type=OutputType.JSON))
        for team_box_score in team_box_scores:
            new_team_box_score = create_team_box_score(team_box_score, date_converted)
            db.session.add(new_team_box_score)
            db.session.commit()
    return str(dates)


@app.route('/teams_season_results')
def teams_season_results():
    path = os.path.join(current_path, '../db/raw/team_season_results.sql')
    path = os.path.abspath(path)
    result = db.session.execute(open(path, 'r').read())
    return jsonify([dict(row) for row in result])


@app.route('/team_list')
def team_list():
    teams = TeamBoxScore.query.with_entities(TeamBoxScore.team).distinct(TeamBoxScore.team).all()
    return teams_box_score_schema.jsonify(teams)


@app.route('/team_season_results/<team>')
def team_season_results(team):
    teams = TeamBoxScore.query.filter_by(team=team).all()
    return teams_box_score_schema.jsonify(teams)


@app.route('/team_players/<team>')
def get_team_players(team):
    players = PlayerSeasonTotals.query.filter_by(team=team).all()
    return players_season_total_schema.jsonify(players)


@app.route('/matches')
def get_matches():
    path = os.path.join(current_path, '../db/raw/matches.sql')
    path = os.path.abspath(path)
    result = db.session.execute(open(path, 'r').read())
    # print([dict(row) for row in result])
    return jsonify([dict(row) for row in result])


@app.route('/percentage_made_by_teams')
def percentage_made_by_teams():
    path = os.path.join(current_path, '../db/raw/percentage_made_by_team.sql')
    path = os.path.abspath(path)
    result = db.session.execute(open(path, 'r').read())
    return jsonify([dict(row) for row in result])


@app.route('/total_stats_by_team')
def total_stats_by_team():
    path = os.path.join(current_path, '../db/raw/total_stats_teams.sql')
    path = os.path.abspath(path)
    result = db.session.execute(open(path, 'r').read())
    return jsonify([dict(row) for row in result])


@app.route('/prediction')
def prediction():
    path = os.path.join(current_path, '../db/raw/matches.sql')
    path = os.path.abspath(path)
    result = db.session.execute(open(path, 'r').read())
    # print([dict(row) for row in result])
    to_json = [dict(row) for row in result]
    # print('Numero de fechas', len(to_json))
    for val in to_json[1:5]:
        date_time_obj = datetime.strptime(str(val['date']), "%Y-%m-%d")
        date_converted = date_time_obj.strftime('%m/%d/%Y')
        result = make_interpret_predictions(str(date_converted), '2019-20', '10/22/2019')
        for team_match_result in result:
            db.session.add(team_match_result)
            db.session.commit()
    return 'buena'
    # result = make_interpret_predictions('12/01/2019', '2019-20', '10/22/2019')
    # for team_match_result in result:
    # db.session.add(team_match_result)
    # db.session.commit()


@app.route('/prediction_result')
def prediction_result():
    path = os.path.join(current_path, '../db/raw/predict_percentage.sql')
    path = os.path.abspath(path)
    result = db.session.execute(open(path, 'r').read())
    games = [dict(row) for row in result]
    season_result = []
    for game in games:
        game_result = define_winner(
            game['home_team'],
            game['prediction_home_team'],
            game['away_team'],
            game['prediction_away_team']
        )
        game['winner'] = game_result[0]
        game['loser'] = game_result[1]
    teams = TeamBoxScore.query.with_entities(TeamBoxScore.team).distinct(TeamBoxScore.team).all()
    for team in teams:
        team = str(team).replace("('", '').replace("',)", '')
        team_season_results = {
            "team": team,
            "total_win": 0,
            "total_loss": 0
        }
        for game in games:
            if game['winner'] == team:
                team_season_results['total_win'] += 1
            elif game['loser'] == team:
                team_season_results['total_loss'] += 1
        season_result.append(team_season_results)
    print(season_result)

    return jsonify({
        "games": games,
        "season_result": season_result
    })


def define_winner(home_team, prediction_home_team, away_team, prediction_away_team):
    if float(np.random.rand()) < float(prediction_home_team):
        return [home_team, away_team]
    else:
        return [away_team, home_team]

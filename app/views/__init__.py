from app import app
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from app.models.player_season_totals import PlayerSeasonTotals
from app.models.player_box_score import PlayerBoxScore
from app.models.team_box_score import TeamBoxScore
from app.schemas.team_box_score import team_box_score_schema, teams_box_score_schema
from app.db import db
from app.models import create_player_season_total, create_player_box_score, create_team_box_score
from sqlalchemy import distinct
import json
from flask import jsonify
from datetime import datetime
import os

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


@app.route('/matches')
def get_matches():
    path = os.path.join(current_path, '../db/raw/matches.sql')
    path = os.path.abspath(path)
    result = db.session.execute(open(path, 'r').read())
    return jsonify([dict(row) for row in result])

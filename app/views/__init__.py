from app import app
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from app.models.player_season_totals import PlayerSeasonTotals
from app.models.player_box_score import PlayerBoxScore
from app.db import db
from app.models import create_player_season_total, create_player_box_score, create_team_box_score
from sqlalchemy import distinct
import json
from flask import jsonify
from datetime import datetime


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


@app.route('/')
def hello_world():
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

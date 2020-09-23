SELECT
	TEAM,
	COUNT(DATE) PARTIDOS_JUGADOS,
	ROUND(SUM(OFFENSIVE_REBOUNDS) / COUNT(DATE)::DECIMAL,3) REBOTES_OFENSIVOS,
	ROUND(SUM(DEFENSIVE_REBOUNDS) / COUNT(DATE)::DECIMAL,3) REBORES_DEFENSIVOS,
	ROUND(SUM(BLOCKS::DECIMAL) / COUNT(DATE)::DECIMAL,3) BLOQUEOS,
	ROUND(SUM(TURNOVERS) / COUNT(DATE)::DECIMAL,3) ROBOS
FROM
	team_box_score
GROUP BY
	TEAM
SELECT
	TEAM, SUM(POINTS) POINTS, T.TOTAL LEAGUE_POINTS, ROUND((100 / T.TOTAL::DECIMAL) * SUM(POINTS)/100,5) PERCENTAGE
FROM
	TEAM_BOX_SCORE,
	(SELECT SUM(POINTS) TOTAL FROM TEAM_BOX_SCORE) T
GROUP BY
	TEAM, T.TOTAL
ORDER BY
	PERCENTAGE DESC
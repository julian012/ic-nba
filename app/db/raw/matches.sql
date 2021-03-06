SELECT
	--TO_CHAR(TO_DATE(PBS.DATE,'YYYY-MM-DD'), 'MM/DD/YYYY') AS DATE,
	TO_DATE(PBS.DATE,'YYYY-MM-DD') AS DATE,
	('{ ' || STRING_AGG(PBS.TEAM || ' : ' || PBS.OPPONENT, ' , ') || ' }') AS GAMES
FROM
	(SELECT DISTINCT
		PBS.DATE,
		PBS.TEAM,
		PBS.OPPONENT,
		PBS.LOCATION
	FROM
		PLAYER_BOX_SCORE PBS
	WHERE
		PBS.LOCATION = 'HOME') PBS
GROUP BY
	PBS.DATE
ORDER BY
    DATE ASC
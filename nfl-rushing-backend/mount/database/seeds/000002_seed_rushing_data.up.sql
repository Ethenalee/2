BEGIN;
    CREATE unlogged TABLE rushing_json (doc json);
	COPY rushing_json FROM '/srv/root/data/seeds/rushing.json';

    INSERT INTO rushings (
        name,
        team_abbreviation,
        position,
        att,
        att_per_game_avg,
        total_rushing_yards,
        rushing_avg_yds_per_att,
        rushing_yds_per_game,
        total_rushing_touch_down,
        lng_rush,
        rushing_1st_down,
        rushing_1st_down_perc,
        rushing_20_plus_yds_each,
        rushing_40_plus_yds_each,
        fum
    )
    SELECT p.*
    FROM rushing_json l
    CROSS JOIN json_to_record(doc) AS p(
        "Player" TEXT,
        "Team" TEXT,
        "Pos" TEXT,
        "Att" TEXT,
        "Att/G" TEXT,
        "Yds" TEXT,
        "Avg" TEXT,
        "Yds/G" TEXT,
        "TD" TEXT,
        "Lng" TEXT,
        "1st" TEXT,
        "1st%" TEXT,
        "20+" TEXT,
        "40+" TEXT,
        "FUM" TEXT
    );

	DROP TABLE rushing_json;

COMMIT;

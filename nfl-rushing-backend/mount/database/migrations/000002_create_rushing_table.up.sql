BEGIN;

    CREATE TABLE IF NOT EXISTS rushings (
        rec_id BIGSERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        team_abbreviation TEXT NOT NULL,
        position TEXT NOT NULL,
        att TEXT NOT NULL,
        att_per_game_avg TEXT NOT NULL,
        total_rushing_yards TEXT NOT NULL,
        rushing_avg_yds_per_att TEXT NOT NULL,
        rushing_yds_per_game TEXT NOT NULL,
        total_rushing_touch_down TEXT NOT NULL,
        lng_rush TEXT NOT NULL,
        rushing_1st_down TEXT NOT NULL,
        rushing_1st_down_perc TEXT NOT NULL,
        rushing_20_plus_yds_each TEXT NOT NULL,
        rushing_40_plus_yds_each TEXT NOT NULL,
        fum TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT current_timestamp,
        updated_At TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT current_timestamp
    );

    CREATE INDEX IF NOT EXISTS idx_rushings_player_name ON rushings(name);

COMMIT;

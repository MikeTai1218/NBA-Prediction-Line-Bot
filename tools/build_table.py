from utils._team_table import NBA_ABBR_ENG_TO_ABBR_CN
import psycopg

connStr = "YOUR NEON DB URL"


def create_table():
    userNames = ["戴廣逸"]
    data = [(userName, "", 0, 0, 0, 0, 0) for userName in userNames]

    teamNames = list(NBA_ABBR_ENG_TO_ABBR_CN.values())
    teamColumns = ",\n".join([f"\"{team}\" TEXT DEFAULT '0 0'" for team in teamNames])

    createSQL = f"""
    CREATE TABLE IF NOT EXISTS LeaderBoard (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        uid TEXT NOT NULL,
        day_points INTEGER DEFAULT 0,
        week_points INTEGER DEFAULT 0,
        month_points INTEGER DEFAULT 0,
        season_points INTEGER DEFAULT 0,
        all_time_points INTEGER DEFAULT 0,
        {teamColumns}
    );
    """

    with psycopg.connect(connStr) as conn:
        with conn.cursor() as cur:
            cur.execute(createSQL)

            for name, uid, dp, wp, mp, sp, atp in data:
                cur.execute(
                    "INSERT INTO LeaderBoard (name, uid, day_points, week_points, month_points, season_points, all_time_points) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, uid, dp, wp, mp, sp, atp),
                )

            conn.commit()


if __name__ == "__main__":
    create_table()

import psycopg
import requests
from bs4 import BeautifulSoup

connStr = "YOUR NEON DB URL"


def get_player_urls():
    output = {}

    response = requests.get("https://www.foxsports.com/nba/teams")
    soup = BeautifulSoup(response.text, "html.parser")
    teams = soup.find("div", class_="entity-list-group")
    teamsUrl = teams.find_all("a")

    for teamUrl in teamsUrl:
        url = f"https://www.foxsports.com{teamUrl.get('href')}-roster"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        playerGroups = soup.find_all("tbody", class_="row-data lh-1pt43 fs-14")
        for playerGroup in playerGroups[:-1]:
            playerContainers = playerGroup.find_all("tr")
            for playerContainer in playerContainers:
                playerInfo = playerContainer.find(
                    "td", class_="cell-entity fs-18 lh-1pt67"
                )
                playerUrl = f"https://www.foxsports.com{playerInfo.find('a').get('href')}-game-log"
                playerName = playerInfo.find("h3").text.strip()
                print(playerName)
                output[playerName] = playerUrl

    return output


def build_player_url_table(output):
    with psycopg.connect(connStr) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS PlayerLink (
                name TEXT PRIMARY KEY,
                link TEXT
            )
            """
            )

            for name, link in output.items():
                cur.execute(
                    "INSERT INTO PlayerLink (name, link) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET link = EXCLUDED.link",
                    (name, link),
                )
        conn.commit()


build_player_url_table(get_player_urls())

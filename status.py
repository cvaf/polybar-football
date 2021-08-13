#!/home/cvaf/.virtualenvs/test/bin/python

import requests
from bs4 import BeautifulSoup
from datetime import datetime

TEAM_NAME = "Manchester United"
TEAM_MAPPING = {
    "Arsenal": "ARS",
    "Aston Villa": "AVL",
    "AFC Bournemouth": "BOU",
    "Brentford": "BRE",
    "Brighton & Hove Albion": "BHA",
    "Brighton and Hove Albion": "BHA",
    "Burnley": "BUR",
    "Chelsea": "CHE",
    "Crystal Palace": "CRY",
    "Everton": "EVE",
    "Fulham": "FUL",
    "Leeds United": "LEE",
    "Leicester City": "LEI",
    "Liverpool": "LIV",
    "Manchester City": "MCI",
    "Manchester United": "MUN",
    "Newcastle United": "NEW",
    "Norwich City": "NOR",
    "Sheffield United": "SHU",
    "Southampton": "SOU",
    "Tottenham Hotspur": "TOT",
    "Watford": "WAT",
    "West Bromwich Albion": "WBA",
    "West Ham United": "WHU",
    "Wolverhampton Wanderers": "WOL",
}

LEAGUE_MAPPING = {
    "Premier League": "PL",
    "Friendly Match": "FR",
    "The FA Cup": "FA",
    "UEFA Champions League": "CL",
    "Europa League": "EL",
    "Carabao Cup": "EFL",
}


def download_soup(team_name: str) -> BeautifulSoup:
    team = team_name.lower().replace(" ", "-")
    url = f"https://www.skysports.com/{team}-fixtures"
    resp = requests.get(url)
    return BeautifulSoup(resp.text, features="lxml")


def parse_match_information(soup: BeautifulSoup) -> dict:
    return {
        "date": soup.find("h4", {"class": "fixres__header2"}).text,
        "league": soup.find("h5", {"class": "fixres__header3"}).text,
        "teams": [
            e.text for e in soup.find_all("span", {"class": "swap-text__target"})[1:3]
        ],
        "time": soup.find("span", {"class": "matches__date"}).text.strip(),
    }


def parse_match(match_info: dict) -> str:

    # Date
    weekday, day, month = match_info["date"].split(" ")
    date = datetime.strptime(
        f"{datetime.now().year}-{day[:-2]}-{month[:3]} {match_info['time']}",
        "%Y-%d-%b %H:%M",
    )

    # Match
    home_team, away_team = match_info["teams"]
    if home_team in TEAM_MAPPING.keys() and away_team in TEAM_MAPPING.keys():
        match = f"{TEAM_MAPPING[home_team]} - {TEAM_MAPPING[away_team]}"
    elif home_team == TEAM_NAME:
        match = f"{away_team} (H)"
    elif away_team == TEAM_NAME:
        match = f"{home_team} (A)"
    else:
        match = ""

    # League
    league = LEAGUE_MAPPING.get(match_info["league"])

    return f" {match} ({league}); {date.strftime('%d/%m %H:%M')} "


if __name__ == "__main__":

    try:
        soup = download_soup(TEAM_NAME)
        match_info = parse_match_information(soup)
        match_string = parse_match(match_info)

    except Exception as e:
        match_string = str(e)

    print(match_string)

#!/home/costas/.virtualenvs/test/bin/python

import requests
from bs4 import BeautifulSoup

TEAM_NAME = "Manchester United" 
TEAM_MAPPING = {
    "Arsenal": "ARS",
    "Aston Villa": "AVL",
    "AFC Bournemouth": "BOU",
    "Brighton & Hove Albion": "BHA",
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

def download_soup(team_name: str) -> BeautifulSoup:
    team = team_name.lower().replace(" ", "-")
    url = f"https://www.espn.com/soccer/team/fixtures/_/id/360/{team}"
    resp = requests.get(url)
    return BeautifulSoup(resp.text, features="lxml")


def parse_html_table(soup: BeautifulSoup, class_name: str) -> list:
    table = soup.find("table", {"class": class_name})
    data = []
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    return [d for d in data[1] if d]

def parse_match(match_info: list) -> str:
    date_info, home_team, _, away_team, time_info, competition, = match_info
    
    # Date
    weekday, month, day = date_info.split(' ')[:3]
    date = f"{day} {month}"
    
    # Time
    time, _m = time_info.split(' ')
    if _m == 'PM':
      time = f"{int(time.split(':')[0])+12}:{time.split(':')[-1]}"
    
    # Match
    if home_team in TEAM_MAPPING.keys() and away_team in TEAM_MAPPING.keys():
      match = f"{TEAM_MAPPING[home_team]} - {TEAM_MAPPING[away_team]}"
    elif home_team == TEAM_NAME:
      match = f"{away_team} (H)"
    elif away_team == TEAM_NAME:
      match = f"{home_team} (A)"
    else:
      match = ''
    
    return f" {match}; {date}, {time} "


if __name__ == "__main__":

    try:
        soup = download_soup(TEAM_NAME)
        match_info = parse_html_table(soup, "Table")
        next_game = parse_match(match_info)

    except:
        next_game = ""

    print(next_game)

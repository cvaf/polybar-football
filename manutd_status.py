import requests
from lxml import html

# Fetch request
resp = requests.get('https://www.espn.com/soccer/team/fixtures/_/id/360/manchester-united')
tree = html.fromstring(resp.text)

xpath_base = '/html/body/div[1]/div/div/div/div/div[5]/div[2]/div[5]/div[1]/div[1]/' +\
             'section/div/section/div[3]/section[1]/div[2]/div/div[2]/table/tbody/tr[1]/'

# Fetch match date
xpath_date = xpath_base + 'td[1]/div'
date = tree.xpath(xpath_date)[0].text
date = date.split(',')[1][1:]

# Fetch match time
xpath_time = xpath_base + 'td[5]/a'
time = tree.xpath(xpath_time)[0].text
time = time.split(' ')[0]

# Fetch the home team
xpath_team1 = xpath_base + 'td[2]/div/a'
team1 = tree.xpath(xpath_team1)[0].text

# Fetch the away team
xpath_team2 = xpath_base + 'td[4]/div/a'
team2 = tree.xpath(xpath_team2)[0].text

# Team abbreviation mapping
team_mapping = {
    'Arsenal': 'ARS',
    'Aston Villa': 'AVL',
    'AFC Bournemouth': 'BOU',
    'Brighton & Hove Albion': 'BHA',
    'Burnley': 'BUR',
    'Chelsea': 'CHE',
    'Crystal Palace': 'CRY',
    'Everton': 'EVE',
    'Leicester City': 'LEI',
    'Liverpool': 'LIV',
    'Manchester City': 'MCI',
    'Manchester United': 'MUN',
    'Newcastle United': 'NEW',
    'Norwich City': 'NOR',
    'Sheffield United': 'SHU',
    'Southampton': 'SOU',
    'Tottenham Hotspur': 'TOT',
    'Watford': 'WAT',
    'West Ham United': 'WHU',
    'Wolverhampton Wanderers': 'WOL'
}

if __name__ == '__main__':

    # Find the abbreviation for each team and create the  match format
    try:
        team1_abv = team_mapping[team1]
        team2_abv = team_mapping[team2]

        match = ' {} - {}; {}, {} '.format(team1_abv, team2_abv, date, time)

    # If we don't have the abbreviation for the opposing team
    # we use a different match format.
    except:

        if team1 == 'Manchester United':
            match = ' {} (H); {}, {} '.format(team2, date, time)

        else:
            match = ' {} (A); {}, {} '.format(team1, date, time)

    print(match)
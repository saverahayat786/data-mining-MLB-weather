import requests
import pandas as pd

def get_mlb_game_data(year):
    base_url = 'https://statsapi.mlb.com/api/v1/schedule'
    start_date = f'{year}-03-30'
    end_date = f'{year}-10-01'

    params = {
        'sportId': 1,
        'startDate': start_date,
        'endDate': end_date,
        'hydrate': 'team,linescore,boxscore',
        'language': 'en'
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    games = []
    for date in data['dates']:
        for game in date['games']:
            game_id = game['gamePk']
            game_url = f'https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore'
            game_response = requests.get(game_url)
            game_data = game_response.json()

            if 'teams' in game_data and 'home' in game_data['teams'] and 'away' in game_data['teams']:
                home_stats = game_data['teams']['home']['teamStats']['batting']
                away_stats = game_data['teams']['away']['teamStats']['batting']

                for team, stats in [('Home', home_stats), ('Away', away_stats)]:
                    singles = stats['hits'] - (stats['doubles'] + stats['triples'] + stats['homeRuns'])
                    total_bases = (singles + 2 * stats['doubles'] + 3 * stats['triples'] + 4 * stats['homeRuns'])

                    game_info = {
                        'Date': game['officialDate'],
                        'Location': game['venue']['name'],
                        'Team': game['teams'][team.lower()]['team']['name'],
                        'Opponent': game['teams']['away' if team == 'Home' else 'home']['team']['name'],
                        'Singles': singles,
                        'Doubles': stats['doubles'],
                        'Triples': stats['triples'],
                        'Home Runs': stats['homeRuns'],
                        'Total Bases': total_bases
                    }
                    games.append(game_info)

    return pd.DataFrame(games)

year = 2023
df = get_mlb_game_data(year)

df.to_csv(f'mlb_games_{year}.csv', index=False)

print(f"Data for {year} has been saved to mlb_games_{year}.csv")

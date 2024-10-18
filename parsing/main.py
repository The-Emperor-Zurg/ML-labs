import requests
import time
import csv

from config import USER_AGENT, BASE_URL, RPS, STATS_KEYS, LEAGUES_URL
from datetime import datetime
from bs4 import BeautifulSoup
from match import Match
from tqdm import tqdm
from requests.exceptions import RequestException

global_last_request_time = time.monotonic()


def get_request_with_rps(url: str, headers: dict = None, rps: int = RPS) -> requests.Response:
    global global_last_request_time
    max_attempts = 3
    attempt = 0
    last_exception = None

    while attempt < max_attempts:
        now = time.monotonic()
        time_to_sleep = global_last_request_time + 1 / rps - now
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)
        global_last_request_time = now

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
            else:
                print(f"Attempt {attempt + 1}: Received status code {response.status_code}. Retrying...")
        except RequestException as e:
            last_exception = e
            print(f"Attempt {attempt + 1}: Request failed with exception: {e}. Retrying...")

        attempt += 1

    raise RuntimeError(f"Failed to fetch {url} after {max_attempts} attempts") from last_exception

def parse_match_url(match_url) -> Match:
    response = get_request_with_rps(match_url, headers={'User-Agent': USER_AGENT})
    bs = BeautifulSoup(response.content, features="html.parser")

    match = bs.find('div', {'class': 'match'})

    match_id = int(match.get('data-id'))
    match_title = match.find('div', {'class': 'match-info__title'}).text.strip()
    total_score = match.find('div', {'class': 'match-info__score-total'}).text.strip()

    team_names = match.find_all('div', {'class': 'match-info__team-name'})
    team_1 = team_names[0].text.strip()
    team_2 = team_names[1].text.strip()

    protocol = match.find('div', {'data-type': 'stats'})
    stats = protocol.find('div', {'class': 'stat-graph'})
    stats_rows = stats.find_all('div', {'class': 'stat-graph__row'})
    stats_dict = {}

    for row in stats_rows:
        attribute = row.find('div', {'class': 'stat-graph__title'}).text.strip()
        if attribute in STATS_KEYS:
            left = 0 if row.find('div', {'class': 'stat-graph__value _left'}) is None else int(
                row.find('div', {'class': 'stat-graph__value _left'}).text.strip())
            right = 0 if row.find('div', {'class': 'stat-graph__value _right'}) is None else int(
                row.find('div', {'class': 'stat-graph__value _right'}).text.strip())

            field_name = STATS_KEYS[attribute]
            stats_dict[f'{field_name}_1'] = left
            stats_dict[f'{field_name}_2'] = right

    match = Match(
        id=match_id,
        url=match_url,
        match_date_title=match_title,
        team_1=team_1,
        team_2=team_2,
        total_score=total_score,
        **stats_dict
    )

    return match


def parse_matches_urls(matches_urls) -> list[Match]:
    matches = []
    for match_url in tqdm(matches_urls, desc='Parsing matches: '):
        match = parse_match_url(match_url)
        matches.append(match)

    return matches


def fetch_matches_urls(league_url: str) -> list[str]:
    response = get_request_with_rps(league_url, headers={'User-Agent': USER_AGENT})
    bs = BeautifulSoup(response.content, features="html.parser")
    table = bs.find('table', {'class': 'results-table'})
    table_body = table.find('tbody')
    matches_cells = table_body.find_all('td', {'class': 'results-table__count _column'})
    matches_urls = [BASE_URL + mc.find('a').get('href') for mc in matches_cells]

    return matches_urls


def get_matches(league_url: str) -> list[Match]:
    matches_urls = fetch_matches_urls(league_url)

    matches = parse_matches_urls(matches_urls)

    return matches


def get_leagues_matches() -> list[Match]:
    all_leagues_matches = []
    for league_url in LEAGUES_URL.values():
        leagues_matches = get_matches(league_url)
        all_leagues_matches.extend(leagues_matches)

    return all_leagues_matches


def write_matches_to_tsv(leagues_matches: list[Match], filename: str) -> None:
    matches_tuples = []
    for match in leagues_matches:
        matches_tuples.append(match.to_tuple())

    with open(filename, 'w') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t')
        writer.writerow(Match.fields())
        writer.writerows(matches_tuples)

    return None


def part_1() -> str:
    leagues_matches: list[Match] = get_leagues_matches()
    file_name = f'matches/leagues_matches_{datetime.today().strftime("%Y_%m_%d_%H_%M_%S")}.tsv'
    write_matches_to_tsv(leagues_matches, file_name)

    return file_name


def part_2(tsv_file: str) -> None:
    # df = load_tsv_to_pd(tsv_file)
    # prepared_df = prepare_df(df)
    # file_name = f'matches/leagues_matches_{datetime.today().strftime("%Y%m%d %H%M%S")}.arff'
    # write_df_to_arff(prepared_df, file_name)
    pass


def main():
    tsv_file = part_1()
    #part_2(tsv_file)


if __name__ == '__main__':
    main()


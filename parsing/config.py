USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' 
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36')

BASE_URL = 'https://www.championat.com'

LEAGUES_URL = {
    # 'eng_23_24': 'https://www.championat.com/football/_england/tournament/5467/result/',
    'eng_22_23': 'https://www.championat.com/football/_england/tournament/5025/result/'
}

RPS = 3

STATS_KEYS = {
    'Удары по воротам': 'shoots_in_target',
    'Фолы': 'falls',
    'Угловые': 'corners',
    'Оффсайды': 'off_side',
    '% владения мячом': 'possession',
    'Штрафные удары': 'free_kicks',
    'Удары от ворот': 'shots_from_gate',
    'Заблокированные удары': 'blocked_shots',
    'Ауты': 'outs',
    'Предупреждения': 'yellow_cards',
    'Удаления': 'red_cards'
}

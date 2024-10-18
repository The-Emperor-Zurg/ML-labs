from dataclasses import dataclass, astuple, fields


@dataclass
class Match:
    id: int
    url: str
    match_date_title: str = ''
    team_1: str = ''
    team_2: str = ''
    total_score: str = ''
    shoots_in_target_1: int = 0
    shoots_in_target_2: int = 0
    falls_1: int = 0
    falls_2: int = 0
    corners_1: int = 0
    corners_2: int = 0
    off_side_1: int = 0
    off_side_2: int = 0
    possession_1: int = 0
    possession_2: int = 0
    free_kicks_1: int = 0
    free_kicks_2: int = 0
    shots_from_gate_1: int = 0
    shots_from_gate_2: int = 0
    blocked_shots_1: int = 0
    blocked_shots_2: int = 0
    outs_1: int = 0
    outs_2: int = 0
    yellow_cards_1: int = 0
    yellow_cards_2: int = 0
    red_cards_1: int = 0
    red_cards_2: int = 0

    def to_tuple(self):
        return astuple(self)

    @classmethod
    def fields(cls):
        return [f.name for f in fields(cls)]

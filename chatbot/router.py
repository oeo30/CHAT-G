import re
from typing import Literal, Optional, Dict
from .constants import TEAM_CODE_MAP, HITTER_HEADERS, PITCHER_HEADERS, STAT_ALIASES, TEAM_HEADERS, PROFILE_LABELS, ALL_NAMES, TEAM_NAME_MAP

def find_player_name(text: str):
    for name in ALL_NAMES:
        if name in text:
            return name
    return None

def find_teamcode(word: str):
    w = word.strip().upper()
    return TEAM_CODE_MAP.get(w) or TEAM_CODE_MAP.get(word.strip())

def route(message: str) -> Dict:
    msg = message.strip()
    name = find_player_name(msg)

    #투수 vs 타자 맞대결
    if "vs" in msg or "맞대결" in msg:
        try:
            m = re.search(r"([A-Za-z가-힣]+)\s+(\S+)\s+vs\s+([A-Za-z가-힣]+)\s+(\S+)", msg, re.IGNORECASE)
        except:
            print("형식: '<팀> <투수명> vs <팀> <타자명>' 예) '롯데 이민석 vs 두산 김민석'")
            return {"tool":"unknown"}
        if m:
            t1, p_name, t2, h_name = m.groups()
            p_team = find_teamcode(t1)
            h_team = find_teamcode(t2)
            return {"tool":"h2h", "p_team":p_team, "p_name":p_name, "h_team":h_team, "h_name":h_name}

    #2025 재밌었던 경기
    if any(k in msg for k in ["재밌는", "재밌었던", "명경기", "인상깊은"]):
        return {"tool":"good_games"}

    #선수 기록
    if name:
        tokens = msg.split()
        if "요약" in msg:
            return {"tool":"player_summary", "name": name} #선수 전체 요약
        for token in tokens: #선수 세부 스탯
            token_upper = token.upper()
            if token_upper in HITTER_HEADERS + PITCHER_HEADERS + PROFILE_LABELS: 
                return {"tool": "player_stat", "name": name, "stat": token_upper}
            if token in STAT_ALIASES:
                return {"tool": "player_stat", "name": name, "stat": STAT_ALIASES[token]} #한국어 약어
        return {"tool":"player_summary", "name": name}
    
    #팀 기록
    for k in TEAM_NAME_MAP.keys():
        if k in msg:
            team = TEAM_NAME_MAP[k]
            for stat in TEAM_HEADERS:
                if stat in msg: #팀 세부 스탯 (ex. 경기, 승률, 연속 등)
                    return {"tool": "team_stat", "team": team, "stat": stat}
            if "요약" in msg:
                return {"tool": "team_summary", "team": team} #팀 전체 요약
            if any(k in msg for k in ["상대전적", "vs", "팀간 전적", "상대 전적", "팀간전적", "전적"]): #팀간 전적
                return {"tool": "team_vs_all", "team": team}
            return {"tool": "team_summary", "team": team} #팀 전체 요약

    return {"tool":"unknown"} #전부 아닐때 unknown
import re
from typing import Literal, Optional, Dict
import pandas as pd
from .constants import TeamCode, TEAM_MAP, HITTER_HEADERS, PITCHER_HEADERS, STAT_ALIASES, TEAM_HEADERS, PROFILE_LABELS

df = pd.read_csv("crawler/playerid.csv")
ALL_NAMES = df["name"].tolist()

def find_name_in_text(text: str):
    for name in ALL_NAMES:
        if name in text:
            return name
    return None

def _teamcode(word: str) -> Optional[TeamCode]:
    w = word.strip().upper()
    return TEAM_MAP.get(w) or TEAM_MAP.get(word.strip())

def route(message: str) -> Dict:
    msg = message.strip()
    name = find_name_in_text(msg)

    # --- 맞대결 ---
    if "vs" in msg or "맞대결" in msg:
        m = re.search(r"([A-Za-z가-힣]+)\s+(\S+)\s+vs\s+([A-Za-z가-힣]+)\s+(\S+)", msg, re.IGNORECASE)
        if m:
            t1, p_name, t2, h_name = m.groups()
            p_team = _teamcode(t1)
            h_team = _teamcode(t2)
            return {"tool":"h2h", "p_team":p_team, "p_name":p_name, "h_team":h_team, "h_name":h_name}

    # --- 팀 요약 ---
    for k, code in TEAM_MAP.items():
        if k in msg:
            for stat in TEAM_HEADERS:
                if stat in msg:
                    return {"tool": "team_stat", "team": code, "stat": stat}
            # 전체 요약
            return {"tool": "team_summary", "team": code}
        if any(k in msg for k in ["상대전적", "vs", "팀간 전적", "상대 전적", "팀간전적"]):
            return {"tool": "team_vs_all", "team": code}

    # --- 선수 요약 / 스탯 ---
    if name:
        tokens = msg.split()
        # 요약
        if "요약" in msg:
            return {"tool":"player_summary", "name": name}
        # 스탯 매핑 (영문/한글 둘 다 처리)
        for token in tokens:
            token_upper = token.upper()
            if token_upper in HITTER_HEADERS + PITCHER_HEADERS + PROFILE_LABELS:
                return {"tool": "player_stat", "name": name, "stat": token_upper}
            if token in STAT_ALIASES:
                return {"tool": "player_stat", "name": name, "stat": STAT_ALIASES[token]}

        return {"tool":"player_summary", "name": name}

    return {"tool":"unknown"}
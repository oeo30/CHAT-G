import re
from typing import Literal, Optional, Tuple, Dict
from .utils import find_name_in_text

TeamCode = Literal["LG","HH","SK","SS","KT","LT","NC","HT","OB","WO"]

TEAM_MAP = {
    "LG":"LG","엘지":"LG",
    "한화":"HH",
    "SSG":"SK","쓱":"SK",
    "삼성":"SS",
    "KT":"KT","케이티":"KT",
    "롯데":"LT","자이언츠":"LT",
    "KIA":"HT","기아":"HT",
    "NC":"NC","엔씨":"NC",
    "두산":"OB",
    "키움":"WO"
}

def _teamcode(word: str) -> Optional[TeamCode]:
    w = word.strip().upper()
    return TEAM_MAP.get(w) or TEAM_MAP.get(word.strip())

def route(message: str) -> Dict:
    """
    간단 라우팅:
      - 'vs' | '맞대결' → h2h (형식: '<팀> <투수명> vs <팀> <타자명>')
      - '순위'/'승률'/'최근10'/'연속'/'홈'/'방문' → team_summary
      - player name 포함 → player_summary (CSV 조회는 상위에서)
      - 그 외 → unknown
    """
    msg = message.strip()
    name = find_name_in_text(msg)
    
    # 1) H2H
    if "vs" in msg or "맞대결" in msg:
        m = re.search(r"([A-Za-z가-힣]+)\s+(\S+)\s+vs\s+([A-Za-z가-힣]+)\s+(\S+)", msg, re.IGNORECASE)
        if m:
            t1, p_name, t2, h_name = m.groups()
            p_team = _teamcode(t1)
            h_team = _teamcode(t2)
            return {"tool":"h2h", "p_team":p_team, "p_name":p_name, "h_team":h_team, "h_name":h_name}

    # 2) 팀 요약 키워드
    if any(k in msg for k in ["롯데 성적","순위","승률","최근10","연속","홈","방문","팀 성적","팀 요약"]):
        return {"tool":"team_summary"}

    # 3) 선수 요약 (라벨만 지정; 실제 타입은 상위에서 get_info로 판단)
    if name:
        # 이름은 상위에서 CSV로 판별
        return {"tool":"player_summary", "name": name}

    return {"tool":"unknown"}
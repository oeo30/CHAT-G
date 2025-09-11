from bs4 import BeautifulSoup #HTML 파싱
from typing import Dict, Any
from .fetch import Fetcher 
from chatbot.constants import TEAM_HEADERS

TEAM_URL = "https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx"
VS_PANEL_ID = "#cphContents_cphContents_cphContents_pnlVsTeam"


def fetch_team(fetcher: Fetcher):
    html = fetcher.get(TEAM_URL)
    soup = BeautifulSoup(html, "lxml")
    team = "롯데"

    #팀 순위 데이터 추출
    rank_table = soup.select_one("table.tData")
    summary = {h: "" for h in TEAM_HEADERS}

    for tr in rank_table.select("tbody tr"):
        tds = [td.get_text(strip=True) for td in tr.select("td")] #테이블에서 행 추출
        if tds[1] == team:
            for i, k in enumerate(TEAM_HEADERS):
                summary[k] = tds[i]
            break

    #팀간 전적 데이터 추출
    vs_dict = {}
    vs_table = soup.select_one(VS_PANEL_ID).select_one("table.tData")
    vs_headers = [th.get_text().replace("\n", "").split("(")[0] for th in vs_table.select("thead th")]
    vs_headers = vs_headers[1:]

    for tr in vs_table.select("tbody tr"): #모든 행 순회
        if tr.select("td")[0].get_text() == team: #팀명 롯데면
            tds = [td.get_text() for td in tr.select("td")] #값 추출
            tds = tds[1:]  
            vs_dict = dict(zip(vs_headers, tds))
            break
    del vs_dict[team]

    return {"team": team, "summary": summary, "vs": vs_dict}
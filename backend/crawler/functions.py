from bs4 import BeautifulSoup #HTML 파싱
from typing import Dict, Any
from .fetch import Fetcher 

BASE = "https://www.koreabaseball.com/Record"
PITCHER_URL = f"{BASE}/Player/PitcherDetail/Basic.aspx?"
HITTER_URL = f"{BASE}/Player/HitterDetail/Basic.aspx?"
TEAM_URL = f"{BASE}/TeamRank/TeamRankDaily.aspx"

VS_PANEL_ID = "#cphContents_cphContents_cphContents_pnlVsTeam"
PROFILE_PANEL_ID = "#cphContents_cphContents_cphContents_playerProfile"

PITCHER_HEADERS = ["ERA","G","CG","SHO","W","L","SV","HLD","WPCT","TBF","NP","IP","H","2B","3B","HR","SAC","SF","BB","IBB","SO","WP","BK","R","ER","BSV","WHIP","AVG","QS"]
HITTER_HEADERS = ["AVG", "G", "PA", "AB", "R", "H", "2B", "3B", "HR", "TB", "RBI", "SB", "CS", "SAC", "SF", "BB", "IBB", "HBP", "SO", "GDP", "SLG", "OBP", "E", "SB%", "MH", "OPS", "RISP", "PH-BA"]
TEAM_HEADERS = ["순위","팀명","경기","승","패","무","승률","게임차","최근10경기","연속","홈","방문"]

def fetch_pitcher(player_id: str, fetcher: Fetcher): #투수 정보 크롤링
    html = fetcher.get(PITCHER_URL, params={"playerID": player_id})
    soup = BeautifulSoup(html, "lxml")

    profile = {
        "player_id": player_id,
        "name": soup.select_one(f"{PROFILE_PANEL_ID}_lblName").get_text(), #CSS 셀렉터로 기본 정보 추출
        "number": soup.select_one(f"{PROFILE_PANEL_ID}_lblBackNo").get_text(),
        "birthday": soup.select_one(f"{PROFILE_PANEL_ID}_lblBirthday").get_text(),   
        "position": soup.select_one(f"{PROFILE_PANEL_ID}_lblPosition").get_text(),
        "body": soup.select_one(f"{PROFILE_PANEL_ID}_lblHeightWeight").get_text(),
        "career": soup.select_one(f"{PROFILE_PANEL_ID}_lblCareer").get_text(),
        'salary': soup.select_one(f"{PROFILE_PANEL_ID}_lblSalary").get_text(),
        "draft": soup.select_one(f"{PROFILE_PANEL_ID}_lblDraft").get_text()
    }

    tables = soup.select("div.tbl-type02 table.tbl.tt")
    table1, table2 = tables[0], tables[1]
    stats = {h: "" for h in PITCHER_HEADERS}

    cells1 = [td.get_text(strip=True) for td in table1.select_one("tbody tr").select("td")]
    cells1 = cells1[1:] #팀명 제외
    keys1 = PITCHER_HEADERS[:17]
    for i, k in enumerate(keys1): #enumerate: 인덱스와 값을 함께 반환
        if i < len(cells1):
            stats[k] = cells1[i] #딕셔너리에 저장

    cells2 = [td.get_text(strip=True) for td in table2.select_one("tbody tr").select("td")]
    keys2 = PITCHER_HEADERS[16:]
    for i, k in enumerate(keys2):
        if i < len(cells2):
            stats[k] = cells2[i]

    return {**profile, **stats}

def fetch_hitter(player_id: str, fetcher: Fetcher): #타자 정보 크롤링
    html = fetcher.get(HITTER_URL, params={"playerID": player_id})
    soup = BeautifulSoup(html, "lxml")

    profile = {
        "player_id": player_id,
        "name": soup.select_one(f"{PROFILE_PANEL_ID}_lblName").get_text(), #CSS 셀렉터로 기본 정보 추출
        "number": soup.select_one(f"{PROFILE_PANEL_ID}_lblBackNo").get_text(),
        "birthday": soup.select_one(f"{PROFILE_PANEL_ID}_lblBirthday").get_text(),
        "position": soup.select_one(f"{PROFILE_PANEL_ID}_lblPosition").get_text(),
        "body": soup.select_one(f"{PROFILE_PANEL_ID}_lblHeightWeight").get_text(),
        "career": soup.select_one(f"{PROFILE_PANEL_ID}_lblCareer").get_text(),
        'salary': soup.select_one(f"{PROFILE_PANEL_ID}_lblSalary").get_text(),
        "draft": soup.select_one(f"{PROFILE_PANEL_ID}_lblDraft").get_text()
    }

    tables = soup.select("div.tbl-type02 table.tbl.tt")
    table1, table2 = tables[0], tables[1]
    stats = {h: "" for h in HITTER_HEADERS}

    cells1 = [td.get_text(strip=True) for td in table1.select_one("tbody tr").select("td")]
    cells1 = cells1[1:]
    keys1 = HITTER_HEADERS[:16]
    for i, k in enumerate(keys1):
        if i < len(cells1):
            stats[k] = cells1[i]

    cells2 = [td.get_text(strip=True) for td in table2.select_one("tbody tr").select("td")]
    keys2 = HITTER_HEADERS[15:]
    for i, k in enumerate(keys2):
        if i < len(cells2):
            stats[k] = cells2[i]

    return {**profile, **stats}

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
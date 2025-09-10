from bs4 import BeautifulSoup #HTML 파싱
from typing import Dict, Any
from .fetch import Fetcher 

BASE = "https://www.koreabaseball.com/Record"
PITCHER_URL = f"{BASE}/Player/PitcherDetail/Basic.aspx?"
HITTER_URL = f"{BASE}/Player/HitterDetail/Basic.aspx?"

PROFILE_PANEL_ID = "#cphContents_cphContents_cphContents_playerProfile"
PITCHER_HEADERS = ["ERA","G","CG","SHO","W","L","SV","HLD","WPCT","TBF","NP","IP","H","2B","3B","HR","SAC","SF","BB","IBB","SO","WP","BK","R","ER","BSV","WHIP","AVG","QS"]
HITTER_HEADERS = ["AVG", "G", "PA", "AB", "R", "H", "2B", "3B", "HR", "TB", "RBI", "SB", "CS", "SAC", "SF", "BB", "IBB", "HBP", "SO", "GDP", "SLG", "OBP", "E", "SB%", "MH", "OPS", "RISP", "PH-BA"]

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
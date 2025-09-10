import time
from bs4 import BeautifulSoup
from typing import Dict, Any
from .fetch import Fetcher

URL = "https://www.koreabaseball.com/Record/Etc/HitVsPit.aspx"
IDS = { # ASP.NET form 요소 ID
    "ddlPitcherTeam":  "ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlPitcherTeam",
    "ddlPitcherPlayer":"ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlPitcherPlayer",
    "ddlHitterTeam":   "ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlHitterTeam",
    "ddlHitterPlayer": "ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlHitterPlayer",
    "btnSearch":       "ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$btnSearch",
}

def form_state(soup: BeautifulSoup) -> dict:
    def val(i): 
        el = soup.select_one(f"#{i}")
        return el.get("value","") if el else ""
    return {
        "__VIEWSTATE": val("__VIEWSTATE"),
        "__VIEWSTATEGENERATOR": val("__VIEWSTATEGENERATOR"),
        "__EVENTVALIDATION": val("__EVENTVALIDATION"),
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
    }

def post(fetcher: Fetcher, data: dict) -> BeautifulSoup:
    html = fetcher.post(URL, data=data)
    return BeautifulSoup(html, "lxml")

def postback_change(fetcher: Fetcher, soup, dropdown_name, value): #드롭다운 값 변경 postback
    data = form_state(soup)
    data[dropdown_name] = value
    data["__EVENTTARGET"] = dropdown_name
    return post(fetcher, data)

def choose_player_value(soup, dropdown_name, player_name) -> str:
    sel = soup.select_one(f"select[name='{dropdown_name}']")
    if not sel: 
        return "0"
    for opt in sel.select("option"):
        if opt.get_text(strip=True) == player_name:
            return opt.get("value","0")
    return "0"

def fetch_hitvspit(p_team: str, p_name: str, h_team: str, h_name: str, fetcher: Fetcher) -> Dict[str, Any]:
    html = fetcher.get(URL)
    soup = BeautifulSoup(html, "lxml")

    soup = postback_change(fetcher, soup, IDS["ddlPitcherTeam"], p_team)
    p_val = choose_player_value(soup, IDS["ddlPitcherPlayer"], p_name)
    data = form_state(soup)

    soup = postback_change(fetcher, soup, IDS["ddlHitterTeam"], h_team)
    h_val = choose_player_value(soup, IDS["ddlHitterPlayer"], h_name)
    data = form_state(soup)

    data[IDS["ddlPitcherTeam"]]  = p_team
    data[IDS["ddlPitcherPlayer"]] = p_val
    data[IDS["ddlHitterTeam"]]   = h_team
    data[IDS["ddlHitterPlayer"]]  = h_val
    data[IDS["btnSearch"]] = "검색"
    soup = post(fetcher, data)

    table = soup.select_one("table.tData.tt")

    body = table.select_one("tbody")
    if body and body.get_text(strip=True) == "기록이 없습니다.":
        return {"status":"empty"}

    headers = [th.get_text(strip=True) for th in table.select("thead th")]
    cells = [td.get_text(strip=True) for td in table.select_one("tbody tr").select("td")]
    
    return {"status":"ok", "pitcher": p_name, "hitter": h_name, **dict(zip(headers, cells))}
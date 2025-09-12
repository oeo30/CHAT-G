from crawler.fetch import Fetcher, get_info 
from crawler.player import fetch_hitter, fetch_pitcher
from crawler.team import fetch_team
from crawler.h2h import fetch_h2h
from .constants import GOOD_GAMES

def handle_player_summary(info: dict, fetcher: Fetcher):
    name = info["name"]
    player_id, ptype = get_info(name)
    if ptype == "hitter":
        data = fetch_hitter(player_id, fetcher)
    elif ptype == "pitcher":
        data = fetch_pitcher(player_id, fetcher)
    for k, v in data.items():
        print(f"{k}: {v}")

def handle_player_stat(info: dict, fetcher: Fetcher):
    name = info["name"]
    stat = info["stat"]
    player_id, ptype = get_info(name)
    if ptype == "hitter":
        data = fetch_hitter(player_id, fetcher)
    elif ptype == "pitcher":
        data = fetch_pitcher(player_id, fetcher)

    print(f"{name}의 {stat}은(는) {data[stat]} 입니다.")

def handle_team_summary(info: dict, fetcher: Fetcher):
    team = info["team"]
    data = fetch_team(team, fetcher)
    summary = data["summary"]

    print(f"{team} 팀 요약")
    for k, v in summary.items():
        if k != "팀명":   
            print(f"{k}: {v}")

def handle_team_stat(info: dict, fetcher: Fetcher):
    team = info["team"]
    stat = info["stat"]
    data = fetch_team(team, fetcher)

    print(f"{team} {stat}: {data['summary'][stat]}")
        
def handle_team_vs_all(info: dict, fetcher: Fetcher):
    team = info["team"]
    data = fetch_team(team, fetcher)
    vs = data["vs"]

    print(f"{team} 상대 전적")
    for opp, record in vs.items():
        print(f"{opp}: {record}")

def handle_h2h(info: dict, fetcher: Fetcher):
    res = fetch_h2h(info["p_team"], info["p_name"], info["h_team"], info["h_name"], fetcher)
    if res["status"] != "ok":
        print(f"맞대결 기록이 없습니다.")
        return
    for k, v in res.items():
        print(f"{k}: {v}")
    

def handle_good_games():
    data = GOOD_GAMES
    print("재밌는 경기 목록")
    for game in data:
        print(game)
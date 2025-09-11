from crawler.fetch import Fetcher, get_info 
from crawler.player import fetch_hitter, fetch_pitcher
from crawler.team import fetch_team
from crawler.hitvspit import fetch_hitvspit
from .constants import GOOD_GAMES

def handle_player_summary(name, fetcher: Fetcher):
    player_id, ptype = get_info(name)
    if ptype == "hitter":
        data = fetch_hitter(player_id, fetcher)
    else:
        data = fetch_pitcher(player_id, fetcher)
    print(data)

def handle_player_stat(name, stat, fetcher: Fetcher):
    player_id, ptype = get_info(name)
    if ptype == "hitter":
        data = fetch_hitter(player_id, fetcher)
    else:
        data = fetch_pitcher(player_id, fetcher)
    if stat in data:
        print(f"{name}의 {stat}는 {data[stat]} 입니다.")
    else:
        print(f"[!] {stat} 데이터를 찾을 수 없습니다.")

def handle_team_summary(fetcher: Fetcher):
    data = fetch_team(fetcher)
    team = data["summary"].get("팀명", data["team"])
    summary = data["summary"]

    print(f"{team} 팀 요약")
    for k, v in summary.items():
        if k != "팀명":   
            print(f"- {k}: {v}")

def handle_team_stat(info: dict, fetcher: Fetcher):
    data = fetch_team(fetcher)
    stat = info["stat"]
    team = data["summary"].get("팀명", info["team"])

    if stat in data["summary"]:
        print(f"{team} {stat}: {data['summary'][stat]}")
    else:
        print(f"[?] {stat} 정보를 찾을 수 없습니다.")
        
def handle_team_vs_all(info: dict, fetcher: Fetcher):
    data = fetch_team(fetcher) 
    team_name = data["summary"]["팀명"]
    vs = data["vs"]

    print(f"{team_name} 상대 전적")
    for opp, record in vs.items():
        print(f"- {opp}: {record}")

def handle_h2h(info: dict, fetcher: Fetcher):
    if not all([info.get("p_team"), info.get("p_name"), info.get("h_team"), info.get("h_name")]):
        print("[!] 형식: '<팀> <투수명> vs <팀> <타자명>' 예) '롯데 이민석 vs 두산 김민석'")
        return
    res = fetch_hitvspit(info["p_team"], info["p_name"], info["h_team"], info["h_name"], fetcher)
    print(res)

def handle_good_games():
    data = GOOD_GAMES;
    print("재밌는 경기 목록")
    for game in data:
        print(game)
import sys
from crawler.fetch import Fetcher, get_info 
from crawler.player import fetch_hitter, fetch_pitcher
from crawler.team import fetch_team
from crawler.hitvspit import fetch_hitvspit
from .router import route

def handle_player_summary(msg: str, name, fetcher: Fetcher):
    player_id, ptype = get_info(name)

    if ptype == "hitter":
        data = fetch_hitter(player_id, fetcher)
    else:
        data = fetch_pitcher(player_id, fetcher)
    print(data)

def handle_team_summary(fetcher: Fetcher):
    data = fetch_team(fetcher)
    print(data)

def handle_h2h(info: dict, fetcher: Fetcher):
    if not all([info.get("p_team"), info.get("p_name"), info.get("h_team"), info.get("h_name")]):
        print("[!] 형식: '<팀> <투수명> vs <팀> <타자명>' 예) '롯데 감보아 vs LG 문보경'")
        return
    res = fetch_hitvspit(info["p_team"], info["p_name"], info["h_team"], info["h_name"], fetcher)
    print(res)

def main():
    print("CHAT-G CLI (q=exit)")
    fetcher = Fetcher()

    while True:
        try:
            msg = input("Q: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break
        if not msg or msg.lower() in ("q","quit","exit"):
            print("프로그램을 종료합니다")
            break

        r = route(msg)
        tool = r["tool"]
        name = r.get("name")

        if tool == "player_summary":
            handle_player_summary(msg, name, fetcher)
        elif tool == "team_summary":
            handle_team_summary(fetcher)
        elif tool == "h2h":
            handle_h2h(r, fetcher)
        else:
            print("[?] 이해하지 못했어요. 예) '롯데 팀 순위', '윤동희 요약', '롯데 감보아 vs LG 문보경'")

if __name__ == "__main__":
    sys.exit(main())
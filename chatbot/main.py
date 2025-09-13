import sys
from .router import route
from .handlers import handle_player_summary, handle_team_summary, handle_h2h, handle_player_stat, handle_team_stat, handle_team_vs_all, handle_good_games
from crawler.fetch import Fetcher

def main():
    print("CHAT-G CLI")
    fetcher = Fetcher()

    while True:
        msg = input("Q: ").strip()
        if msg.lower() in ("q","quit"):
            print("프로그램을 종료합니다")
            break

        r = route(msg)
        tool = r["tool"]

        if tool == "player_summary":
            handle_player_summary(r, fetcher)
        elif tool == "player_stat":
            handle_player_stat(r, fetcher)
        elif tool == "team_summary":
            handle_team_summary(r, fetcher)
        elif tool == "team_stat":
            handle_team_stat(r, fetcher)
        elif tool == "team_vs_all":
            handle_team_vs_all(r, fetcher)
        elif tool == "h2h":
            handle_h2h(r, fetcher)
        elif tool == "good_games":
            handle_good_games()
        else:
            print("[?] 이해하지 못했어요. 예) 롯데 순위, 전민재 요약, 윤동희 OPS, 롯데 이민석 vs 두산 김민석")

if __name__ == "__main__":
    sys.exit(main())
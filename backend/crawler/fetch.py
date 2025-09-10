import requests #HTTP 요청 
import pandas as pd
import json
import os

def get_info(name: str):
    df = pd.read_csv("crawler/playerid.csv")
    id = df[df["name"] == name].iloc[0]["id"] #iloc로 실제 값 추출
    type = df[df["name"] == name].iloc[0]["type"]
    return id, type

class Fetcher:
    def __init__(self):
        self.sess = requests.Session() #세션 객체 생성
        self.sess.headers.update({
            "User-Agent": "CHAT-G crawler",
        })

    def get(self, url: str, params: dict = None) -> str: #HTTP GET 요청 보내고 응답
        resp = self.sess.get(url, params=params, timeout=10) 
        resp.raise_for_status() #에러면 예외 발생
        return resp.text 

    def post(self, url: str, data: dict) -> str:
        resq = self.sess.post(url, data=data, timeout=10)
        resq.raise_for_status()
        return resq.text

if __name__ == "__main__": #테스트코드
    from .player import fetch_hitter, fetch_pitcher
    from .team import fetch_team
    from .hitvspit import fetch_hitvspit

    f = Fetcher()

    # player_id, type = get_info("손호영")
    # if type == "hitter":
    #     data = fetch_hitter(player_id, f)
    # elif type == "pitcher":
    #     data = fetch_pitcher(player_id, f)

    data = fetch_hitvspit("LT", "박세웅", "LG", "문보경", f)
    print(data)

    #json 파일로 결과 저장
    filepath = "crawler/results.json"
    save_data = {
        "data": data
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2,default=str)
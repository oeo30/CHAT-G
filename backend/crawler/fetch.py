import requests #HTTP 요청 

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

if __name__ == "__main__": #테스트코드
    from .functions import fetch_hitter, fetch_pitcher, fetch_team

    f = Fetcher()
    player_id = 52568 
    data = fetch_hitter(player_id, f)
    print(data)  # 터미널에 dict 출력
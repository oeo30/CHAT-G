from crawler.fetch import Fetcher, get_info 
from crawler.player import fetch_hitter, fetch_pitcher
from crawler.team import fetch_team
from crawler.h2h import fetch_h2h
from chatbot.constants import GOOD_GAMES

def handle_player_summary_streamlit(info: dict, fetcher: Fetcher):
    """선수 요약 정보를 Streamlit용으로 포맷팅"""
    name = info["name"]
    player_id, ptype = get_info(name)
    if ptype == "hitter":
        data = fetch_hitter(player_id, fetcher)
    elif ptype == "pitcher":
        data = fetch_pitcher(player_id, fetcher)
    
    data.pop("id")
    result = f"**{name} 선수 요약**\n\n"
    for k, v in data.items():
        if k in ["이름", "등번호", "생년월일", "포지션", "신체", "경력", "연봉", "드래프트"]:
            result += f"• {k}: {v}  \n"
        else:
            result += f"{k}: {v}, "
    return result

def handle_player_stat_streamlit(info: dict, fetcher: Fetcher):
    """선수 특정 스탯을 Streamlit용으로 포맷팅"""
    name = info["name"]
    stat = info["stat"]
    player_id, ptype = get_info(name)
    if ptype == "hitter":
        data = fetch_hitter(player_id, fetcher)
    elif ptype == "pitcher":
        data = fetch_pitcher(player_id, fetcher)

    return f"**{name}의 {stat}**: {data[stat]}"

def handle_team_summary_streamlit(info: dict, fetcher: Fetcher):
    """팀 요약 정보를 Streamlit용으로 포맷팅"""
    team = info["team"]
    data = fetch_team(team, fetcher)
    summary = data["summary"]

    result = f"**{team} 팀 요약**\n\n"
    for k, v in summary.items():
        if k != "팀명":   
            result += f"• {k}: {v}  \n"
    return result

def handle_team_stat_streamlit(info: dict, fetcher: Fetcher):
    """팀 특정 스탯을 Streamlit용으로 포맷팅"""
    team = info["team"]
    stat = info["stat"]
    data = fetch_team(team, fetcher)

    return f"**{team} {stat}**: {data['summary'][stat]}"
        
def handle_team_vs_all_streamlit(info: dict, fetcher: Fetcher):
    """팀 상대 전적을 Streamlit용으로 포맷팅"""
    team = info["team"]
    data = fetch_team(team, fetcher)
    vs = data["vs"]

    result = f"**{team} 상대 전적**\n\n"
    for opp, record in vs.items():
        result += f"• {opp}: {record}  \n"
    return result

def handle_h2h_streamlit(info: dict, fetcher: Fetcher):
    """투수 vs 타자 맞대결을 Streamlit용으로 포맷팅"""
    res = fetch_h2h(info["p_team"], info["p_name"], info["h_team"], info["h_name"], fetcher)
    if res["status"] != "ok":
        return "맞대결 기록이 없습니다."
    
    result = f"**{info['p_name']} vs {info['h_name']} 맞대결**\n\n"
    for k, v in res.items():
        if k != "status":
            result += f"• {k}: {v}  \n"
    return result

def handle_good_games_streamlit():
    """재밌는 경기 목록을 Streamlit용으로 포맷팅"""
    data = GOOD_GAMES
    result = "**재밌는 경기 목록**\n\n"
    for i, game in enumerate(data, 1):
        result += f"{i}. {game}  \n"
    return result

import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="CHAT-G (롯데자이언츠 챗봇)",
    page_icon="⚾",
)

from chatbot.router import route
from crawler.fetch import Fetcher
from app.streamlit_handlers import (
    handle_player_summary_streamlit,
    handle_player_stat_streamlit,
    handle_team_summary_streamlit,
    handle_team_stat_streamlit,
    handle_team_vs_all_streamlit,
    handle_h2h_streamlit,
    handle_good_games_streamlit
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    @font-face {
    font-family: 'Giants';
    src: url('https://cdn.jsdelivr.net/gh/fonts-archive/Giants/Giants-Regular.ttf') format('truetype');
    }
            
    @font-face {
    font-family: 'Giants Inline';
    src: url('https://cdn.jsdelivr.net/gh/fonts-archive/GiantsInline/GiantsInline.ttf') format('truetype');
    }
    
    /* 전체 배경색 */
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Giants';
    }
    
    /* 채팅 메시지 스타일 */
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    /* 제목 스타일 */
    h1 {
        font-family: 'Giants Inline' !important;
        color: #1976d2;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 3rem;
        font-weight: normal;
    }
    
</style>
""", unsafe_allow_html=True)

st.title("CHAT-G")
st.caption("2025시즌 롯데 자이언츠 스탯 챗봇")

# Fetcher 초기화
@st.cache_resource
def get_fetcher():
    return Fetcher()

fetcher = get_fetcher()

# 채팅 히스토리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("질문을 입력하세요. 예) 롯데 순위, 전민재 요약, 윤동희 OPS"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # 라우팅 및 처리
        try:
            r = route(prompt)
            tool = r["tool"]
            
            response_content = ""
            
            if tool == "player_summary":
                response_content = handle_player_summary_streamlit(r, fetcher)
            elif tool == "player_stat":
                response_content = handle_player_stat_streamlit(r, fetcher)
            elif tool == "team_summary":
                response_content = handle_team_summary_streamlit(r, fetcher)
            elif tool == "team_stat":
                response_content = handle_team_stat_streamlit(r, fetcher)
            elif tool == "team_vs_all":
                response_content = handle_team_vs_all_streamlit(r, fetcher)
            elif tool == "h2h":
                response_content = handle_h2h_streamlit(r, fetcher)
            elif tool == "good_games":
                response_content = handle_good_games_streamlit()
            else:
                response_content = "[?] 이해하지 못했어요. 예) 롯데 순위, 전민재 요약, 윤동희 OPS, 롯데 이민석 vs 두산 김민석"
            
            st.markdown(response_content)
            
        except Exception as e:
            error_msg = f"오류가 발생했습니다: {str(e)}"
            st.error(error_msg)
            response_content = error_msg
        
        # 어시스턴트 응답 추가
        st.session_state.messages.append({"role": "assistant", "content": response_content})
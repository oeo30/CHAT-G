# st_chatbot.py
import google.generativeai as genai 
import streamlit as st
import os
from dotenv import load_dotenv

# 환경 변수에서 project_root 가져오기
project_root = os.environ.get("PROJECT_ROOT", "/Users/taknayeon/Development/Projects/CHAT-G")
load_dotenv()

st.title("Gemini-Bot")

@st.cache_resource
def get_model():
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # 최신 경량 모델
    return model

model = get_model()

if "chat_session" not in st.session_state:    
    st.session_state["chat_session"] = model.start_chat(history=[]) 

for content in st.session_state.chat_session.history:
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)

if prompt := st.chat_input("메시지를 입력하세요."):    
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)        
        st.markdown(response.text)


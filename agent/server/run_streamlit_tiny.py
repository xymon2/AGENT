import streamlit as st
import time
from tinydb import TinyDB, Query

from agent.components.chains.rags import make_mydata_ragchain
from streamlit.runtime.scriptrunner import get_script_run_ctx

session_id = get_script_run_ctx().session_id

db = TinyDB('agent/resources/db/tinydb.json')
Session = Query()
table = db.table('chat_sessions')

session_data = table.search(Session.session_id == session_id)
if not session_data:
    print("Initializing chat session data")
    table.insert({"session_id": session_id, "conversation_history": [], "loading": False})
    session_data = table.search(Session.session_id == session_id)

mydata_agent = make_mydata_ragchain()

st.title("마이데이터 AI Agent")
query = st.text_input("질문을 입력하세요:", placeholder="예: 개인신용정보 전송에서 즉시전송에 대해 설명해줘", key='user_query')

chat_history = session_data[0]['conversation_history']
loading = session_data[0]['loading']

def test_response(query):
    time.sleep(5)
    return f"{query}에대한 답변입니다."

def get_response():
    query = st.session_state["user_query"]
    if query:
        if not loading:
            table.update({'loading': True}, Session.session_id == session_id)

            with st.spinner("AI 에이전트가 답변을 생성 중입니다. 잠시만 기다려주세요..."):
                response = test_response(query)
                # 가장최근 5개의 대화를 사용해서 답변을 생성합니다.
                # response = mydata_agent.get_response(query, chat_history[-5:])

                chat_history.append({"role": "user", "content": query})
                chat_history.append({"role": "agent", "content": response})
                table.update({'conversation_history': chat_history}, Session.session_id == session_id)
        
                table.update({'loading': False}, Session.session_id == session_id)
                print(f"Response generated successfully for query: {query}")
        else:
            st.warning("AI 에이전트가 현재 답변을 생성 중입니다. 잠시만 기다려주세요.")

    else:
        st.write("질문을 입력해주세요.")

if loading:
    st.warning("AI 에이전트가 현재 답변을 생성 중입니다. 잠시만 기다려주세요.")
    time.sleep(3)
    st.rerun()

st.button(
    "답변 받기", 
    on_click=get_response, 
    disabled=loading,
)

for message in chat_history:
    if message["role"] == "user":
        st.write(f"👩‍💻 : {message['content']}")
    else:
        st.write(f"🤖 : {message['content']}")


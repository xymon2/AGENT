import streamlit as st
import time

from agent.components.chains.rags import make_mydata_ragchain
from streamlit.runtime.scriptrunner import get_script_run_ctx

session_id = get_script_run_ctx().session_id

if session_id not in st.session_state:
    st.session_state[session_id] = {"conversation_history": [], "loading": False}

mydata_agent = make_mydata_ragchain()

st.title("마이데이터 AI Agent")
query = st.text_input("질문을 입력하세요:", placeholder="예: 개인신용정보 전송에서 즉시전송에 대해 설명해줘", key='user_query')

chat_history = st.session_state[session_id]["conversation_history"]
print(st.session_state[session_id])

def test_response(query):
    time.sleep(5)
    return f"{query}에대한 답변입니다."

def get_response():
    query = st.session_state["user_query"]
    if query:
        if not st.session_state[session_id]["loading"]:
            st.session_state[session_id]["loading"] = True
            with st.spinner("AI 에이전트가 답변을 생성 중입니다. 잠시만 기다려주세요..."):
                # response = test_response(query)
                # 가장최근 5개의 대화를 사용해서 답변을 생성합니다.
                response = mydata_agent.get_response(query, chat_history[-5:])

                chat_history.append({"role": "user", "content": query})
                chat_history.append({"role": "agent", "content": response})
        
                st.session_state[session_id]["loading"] = False
                print(f"done generating response for query: {query}")
        else:
            st.warning("AI 에이전트가 현재 답변을 생성 중입니다. 잠시만 기다려주세요.")

    else:
        st.write("질문을 입력해주세요.")

if st.session_state[session_id]["loading"]:
    st.warning("AI 에이전트가 현재 답변을 생성 중입니다. 잠시만 기다려주세요.")
    time.sleep(3)
    st.rerun()

st.button(
    "답변 받기", 
    on_click=get_response, 
)

for message in chat_history:
    if message["role"] == "user":
        st.write(f"👩‍💻 : {message['content']}")
    else:
        st.write(f"🤖 : {message['content']}")


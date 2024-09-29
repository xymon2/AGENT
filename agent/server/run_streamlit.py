import streamlit as st

from agent.components.chains.rags import make_mydata_ragchain

user_id = "user_id"

if user_id not in st.session_state:
    st.session_state[user_id] = {"conversation_history": []}

mydata_agent = make_mydata_ragchain()

st.title("마이데이터 AI Agent")
query = st.text_input("질문을 입력하세요:", placeholder="예: 개인신용정보 전송에서 즉시전송에 대해 설명해줘")

chat_history = st.session_state[user_id]["conversation_history"]

if st.button("답변받기"):
    if query:
        response = mydata_agent.get_response(query)

        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "agent", "content": response})
        
        print(chat_history)
        for message in chat_history:
            if message["role"] == "user":
                st.write(f"👩‍💻 : {message['content']}")
            else:
                st.write(f"🤖 : {message['content']}")

    else:
        st.write("질문을 입력해주세요.")
import streamlit as st

from agent.components.chains.rags import make_mydata_ragchain


mydata_agent = make_mydata_ragchain()

st.title("마이데이터 AI Agent")
query = st.text_input("질문을 입력하세요:", placeholder="예: 개인신용정보 전송에서 즉시전송에 대해 설명해줘")

if st.button("답변받기"):
    if query:
        response = mydata_agent.get_response(query)
        st.write("**답변**:")
        st.write(response)
    else:
        st.write("질문을 입력해주세요.")

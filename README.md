## 실행방법
poetry run streamlit run agent/server/run_streamlit_tiny.py  

## 멀티턴
기존 대화기록 최근 5개만 넣음으로써 토큰을 아끼면서 멀티턴 진행을하도록함
```python
response = mydata_agent.get_response(query, chat_history[-5:])
```

## 프로젝트 구조
메인구조는 다음과같다.
```
agent/components
    /chains
        /rags
            /vectorstore_retreival.py
    /embeddings
        /openai_builder.py
    /knowledges
        /pdf
        loader.py
    /llms
        /openai_builder.py
    /vectorstores
        /faiss_index
        faiss_builder.py
    /sever
        /run_streamlit_tiny.py
        /run_streamlit.py

```

1. 다양한 모델 제공가능
embedding, llms 하위에 다양한 모델들을 작성 후, vector store및 chain에서 원하는 조합으로 갈아낄 수 있도록 했습니다.(langchain framework에서 제공하는 모델이어야 합니다.)  
원하는 타입의 retrieval.py에서, make_{purpose}_ragchain 등의 함수에서 특정 용도의 체인에서 가장 적합한 모델조합을 만들어 생성할 수 있도록 했습니다.

2. knowledge load + idx
미리 vector store index를 준비해놓았습니다
추가로 데이터를 준비해서 새로 index를 만드려면 faiss_builder.py를 실행시키면 됩니다.

3. 동시성
streamlit의 session만 이용해서는 동시성처리가 잘 안되는 부분이 있고, 오픈 소스 db등 외부 툴을 이용하면 좋지만 테스트 세팅이 힘들어, tiny db라는 라이브러리로 간단한 세션을 관리하도록 했습니다.  

streamlit의 session id기반으로 현재까지의 대화와 loading status를 관리해 loading == True이면(이미 진행중인 요청이있다면) 요청을 block하도록 했습니다.

4. token 관리
api key를 , 로 구분하도록 환경변수에서 받고, 그중에서 랜덤하게 모델 생성시 선택하도록 했습니다.
이때 429 - rate limit, insufficient quota시 해당 부분을 다시 reset해서 다시 api key를 선택하도록 했습니다.
일단 random 으로 고르고 있지만, round-robin 혹은 어딘가의 토큰을 기록할 수 있다면 글로벌하게 key 별로 토큰을 트랙킹하여 적절한 key를 고르는 알고리즘을 추가할 수 도 있을 것 같습니다.

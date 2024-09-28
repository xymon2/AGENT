from agent.components.embeddings import OpenAIEmbBuilder
from agent.components.llms import OpenAILLMBuilder
from agent.components.vectorstores import FaissBuilder

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class VectorStoreRetriever():
    def __init__(self, llm = None, vector_store = None, prompt = None, top_k=5):
        if llm is None:
            raise ValueError("llm must be provided")

        if vector_store is None:
            raise ValueError("vector_store must be provided")
        
        if prompt is None:
            raise ValueError("prompt must be provided")
        
        self.retriever = vector_store
        self.top_k = top_k

        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser
        

    def get_documents(self, query):
        docs = self.retriever.retrieve(query, k=self.top_k)
        return docs

    def get_response(self, query):
        retrieved_docs = self.get_documents(query)
        retrieved_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
        return self.chain.invoke({"knowledge": retrieved_text, "question": query})


def make_mydata_ragchain():
    llm_model_type = "openai"
    llm_model_name ="gpt-4"
    llm_temperature = 0

    openai_key = ""

    llm = OpenAILLMBuilder(
        model_type=llm_model_type,
        model_name=llm_model_name,
        temperature=llm_temperature,
        api_key = openai_key,
    ).get_model()

    emb_model_type = "openai"
    emb_model_name = "text-embedding-3-large"
    emb = OpenAIEmbBuilder(model_type=emb_model_type, model_name=emb_model_name,api_key=openai_key).get_model()

    vector_store = FaissBuilder(
        embeddings = emb,
        documents = None,
        local_index_path="agent/components/vectorstores/faiss_index"
    )

    prompt = ChatPromptTemplate.from_template('''
    당신은 마이데이터 관련 전문가입니다. 주어진 데이터베이스(Knowledge) 내에서만 정보를 검색해 답변하세요. 
    질문에 답변할 때는 아래 조건을 따르세요:

    1. **오직 Knowledge 데이터에만 기반한 답변을 생성**하세요. Knowledge에 없는 정보는 제공하지 마세요.
    2. 여러 개의 Knowledge를 사용해도 됩니다.
    3. **관련 정보가 없을 경우**: 질문에 대한 답을 Knowledge에서 찾을 수 없으면, "관련 정보를 찾을 수 없습니다"라고만 답변하세요.
    4. 답변의 마지막에 더 궁금하신점이 없는지 꼭 물어보세요.
    5. 마지막에 출처를 명시하세요.

    **질문**: 마이데이터 서비스에서 개인정보는 어떻게 관리되나요?

    **Knowledge 1**:
    "마이데이터 서비스는 데이터를 안전하게 보호하기 위해 암호화 기술을 사용합니다."  [출처: "사용자는 본인의 데이터를 제3자와 안전하게 공유할 수 있습니다."]

    **Knowledge 2**:
    "사용자는 본인의 데이터를 제3자와 안전하게 공유할 수 있습니다."  [출처: "사용자는 본인의 데이터를 제3자와 안전하게 공유할 수 있습니다."]

    **답변**:
    마이데이터 서비스에서는 사용자가 본인의 데이터를 안전하게 보호하고, 제3자와 안전하게 공유할 수 있도록 암호화 기술을 사용합니다. [출처: "마이데이터 서비스는 데이터를 안전하게 보호하기 위해 암호화 기술을 사용합니다."]

    <Knowledge> : {knowledge} <질문>: {question}'''
    )

    return VectorStoreRetriever(llm, vector_store, prompt, top_k=10)


if __name__ == "__main__":
    mydata_agent = make_mydata_ragchain()
    query = "개인신용정보 전송에서 즉시전송에 대해 설명해줘"
    response = mydata_agent.get_response(query)
    print(response)

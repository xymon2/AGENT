import faiss
from langchain_community.vectorstores import FAISS
from agent.components.embeddings import OpenAIEmbBuilder
from agent.components.knowledges import load_all_pdf_knowledges

from agent.config import config

class FaissBuilder():
    def __init__(self, embeddings, documents = None, local_index_path=None):
        if documents is not None and local_index_path is not None:
            # only documents init
            self.vector_store = FAISS.from_documents(documents, embedding = embeddings)
        elif local_index_path is not None:
            # only local_index_path init
            self.vector_store = FAISS.load_local(local_index_path, embeddings, allow_dangerous_deserialization=True)
        else:
            raise ValueError("Either documents or local_index_path must be provided")
            
        self.local_index_path = local_index_path
    
    def get_model(self):
        return self.vector_store
    
    def retrieve(self, query, k=5):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        return retriever.invoke(query)

    def save_local(self):
        self.vector_store.save_local(self.local_index_path)

if __name__ == "__main__":

    print("load documents and save them as faiss index")
    faiss_idx_path = config.get_faiss_idx_path()
    openai_keys = config.get_openai_api_keys()
    emb = OpenAIEmbBuilder("openai", api_keys = openai_keys).get_model()

    print("loading pdf knowledges...")
    knowledge_pdf_path = config.get_knowledge_pdf_path()
    documents = load_all_pdf_knowledges(knowledge_pdf_path)

    faiss = FaissBuilder(embeddings = emb, documents = documents, local_index_path=faiss_idx_path)

    print("saving faiss index...")
    faiss.save_local()

    print("done")


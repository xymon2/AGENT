import faiss
from langchain_community.vectorstores import FAISS
from agent.server.embeddings import OpenAIEmbProvider
from agent.server.knowledges import load_all_pdf_knowledges

class FaissProvider():
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
    
    def retrieve(self, query, k=5):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        return retriever.invoke(query)

    def save_local(self):
        self.vector_store.save_local(self.local_index_path)

if __name__ == "__main__":
    print("load document and save faiss index")
    faiss_idx_path = "agent/server/vectorstores/faiss_index"
    emb = OpenAIEmbProvider("openai").get_model()

    print("loading document...")
    documents = load_all_pdf_knowledges("agent/server/knowledges/*")
    faiss = FaissProvider(embeddings = emb, documents = documents, local_index_path=faiss_idx_path)

    print("saving faiss index...")
    faiss.save_local()

    print("done")


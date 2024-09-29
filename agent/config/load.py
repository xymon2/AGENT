import os
from dotenv import load_dotenv

class Config:
    def __init__(self, env_type = "local"):
        if env_type == "development":
            env_file_path = "agent/config/dev.env"
        elif env_type == "production":
            env_file_path = "agent/config/prod.env"
        elif env_type == "local":
            env_file_path = "agent/config/local.env"
        else:
            raise ValueError("env_type must be either 'development', 'production' or 'local'")
        
        load_dotenv(env_file_path)
        
        self._openai_api_keys = os.getenv("OPENAI_API_KEYS").split(",")
        self._faiss_idx_path = os.getenv("FAISS_IDX_PATH")
        self._knowledge_pdf_path = os.getenv("KNOWLEDGE_PDF_PATH")
    
    def get_openai_api_keys(self):
        return self._openai_api_keys
    
    def get_faiss_idx_path(self):
        return self._faiss_idx_path

    def get_knowledge_pdf_path(self):
        return self._knowledge_pdf_path

config = Config()

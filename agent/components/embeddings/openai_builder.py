from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
import random

class OpenAIEmbBuilder:
    def __init__(self, model_type: str = "openai", model_name="text-embedding-3-large", api_keys: list[str] = []):
        idx = random.randint(0, len(api_keys) - 1)
        api_key = api_keys[idx]

        if model_type == "openai":
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-large",
                api_key=api_key
            )
        #  for additional models
        # elif model_type == "azure":
        #         self.embeddings = AzureOpenAIEmbeddings(
        #             model_name="",
        #             api_key=api_key
        #         )
        else:
            raise ValueError("Invalid model type")

    def get_model(self):
        return self.embeddings

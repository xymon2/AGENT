from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings

class OpenAIEmbProvider:
    def __init__(self, model_type: str api_key: str = None):
        api_key = ""

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

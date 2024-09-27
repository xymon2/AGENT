from langchain_openai import OpenAI, OpenAIEmbeddings, AzureOpenAI, AzureOpenAIEmbeddings

class OpenAILLMProvider:
    def __init__(self, model_type: str, api_key: str = None):
        api_key = ""

        if model_type == "openai":
            self.model = OpenAI(
                model_name="gpt-3.5-turbo-instruct",
                api_key=api_key,
                temperature=0.5,
                max_retries=2
            )
        # for additional models
        # elif model_type == "azure":
        #     self.model = AzureOpenAI(
        #         model_name="",
        #         api_key=api_key
        # )

        else:
            raise ValueError("Invalid model type")
    
    def get_model(self):
        return self.model

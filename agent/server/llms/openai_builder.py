from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings, AzureOpenAI, AzureOpenAIEmbeddings

class OpenAILLMBuilder:
    def __init__(
        self, 
        model_type: str = "openai", 
        model_name:str = "gpt-4", 
        temperature:int=0,
        api_key: str = None,
    ):
        if model_type == "openai":
            # legacy models
            if "gpt-3" in model_name:
                self.model = OpenAI(
                    model_name=model_name,
                    api_key=api_key,
                    temperature=temperature,
                    max_retries=2
                )
            else:
                self.model = ChatOpenAI(
                    model_name=model_name,
                    api_key=api_key,
                    temperature=temperature,
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

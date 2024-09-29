from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings, AzureOpenAI, AzureOpenAIEmbeddings
import random

class OpenAILLMBuilder:
    def __init__(
        self, 
        model_type: str = "openai", 
        model_name:str = "gpt-4", 
        temperature:int=0,
        api_keys: list[str] = [],
    ):

        idx = random.randint(0, len(api_keys) - 1)
        self._api_keys = api_keys
        self.model_type = model_type
        self.model_name = model_name
        self.temperature = temperature
        api_key = api_keys[idx]

        self.model = self.create_model(model_name, model_type, temperature, api_key)

    def get_model(self):
        return self.model
    
    def create_model(self, model_name, model_type, temp, api_key):
        if self.model_type == "openai":
            # legacy models
            if "gpt-3" in model_name:
                return OpenAI(
                    model_name=model_name,
                    api_key=api_key,
                    temperature=self.temperature,
                    max_retries=2
                )
            else:
                return ChatOpenAI(
                    model_name=model_name,
                    api_key=api_key,
                    temperature=self.temperature,
                    max_retries=2
                )
        # for additional models
        # elif self.model_type == "azure":
        #     return AzureOpenAI(
        #         model_name="",
        #         api_key=api_key
        #     )
        else:
            raise ValueError("Invalid model type")
    
    def reset_model(self):
        idx = random.randint(0, len(self._api_keys) - 1)
        api_key = self._api_keys[idx]
        self.model = self.create_model(self.model_name, self.model_type, self.temperature, api_key)
        return self.model


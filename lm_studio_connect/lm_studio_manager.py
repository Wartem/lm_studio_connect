import requests
from requests.exceptions import RequestException
from lm_studio_connect.utils.constants import VALID_LM_STUDIO_PARAMS


class LMStudioManager:  
    def __init__(self, base_url="http://localhost:1234"):
        self.base_url = base_url

    def get_status_and_loaded_models(self):
        try:
            response = requests.get(f"{self.base_url}/v1/models")
            response.raise_for_status()
            loaded_models = response.json()["data"]
            return (
                {"status": "active", "models": [model["id"] for model in loaded_models]}
                if loaded_models
                else {"status": "idle", "models": []}
            )
        except RequestException as e:
            return {"status": "error", "message": str(e)}
        
    def is_lm_studio_active(self):
        return self.get_status_and_loaded_models()["status"] == "active"

    def is_model_loaded(self, model):
        models_statuses = self.get_status_and_loaded_models()["models"]
        return any(model in m for m in models_statuses)

    def get_loaded_models(self):
        return self.get_status_and_loaded_models()["models"]

    def send_prompt(self, prompt, model_config, **kwargs):
        payload = {
            "prompt": prompt,
            "model": model_config,
        }

        # Only add parameters to payload if they are provided and valid
        for param in VALID_LM_STUDIO_PARAMS:
            if param in kwargs:
                payload[param] = kwargs[param]

        try:
            response = requests.post(f"{self.base_url}/v1/completions", json=payload)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": str(e)}

    def send_chat(self, messages, model_name, **kwargs):
        payload = {
            "messages": messages,
            "model": model_name,
        }

        # Only add parameters to payload if they are provided and valid
        for param in VALID_LM_STUDIO_PARAMS:
            if param in kwargs:
                payload[param] = kwargs[param]

        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions", json=payload
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": str(e)}

    def generate_embedding(self, input_text, model_name):
        try:
            response = requests.post(
                f"{self.base_url}/v1/embeddings",
                json={"input": input_text, "model": model_name},
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": f"An error occurred: {e}"}
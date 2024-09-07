import requests
import json
import functools
from requests.exceptions import RequestException
from lm_studio_connect.utils.constants import VALID_LM_STUDIO_PARAMS
from lm_studio_connect.models.model_manager import LMStudioModelManager


def handle_api_errors(response_handler):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                response.raise_for_status()
                response_json = response.json()
                return response_handler(response_json)
            except RequestException as e:
                print("Request exception:", str(e))  # Debug print
                return {"error": f"Request error: {str(e)}"}
            except json.JSONDecodeError as e:
                print("JSON decoding error:", str(e))  # Debug print
                return {"error": f"JSON decoding error: {str(e)}"}

        return wrapper

    return decorator


def chat_response_handler(response_json):
    if "choices" in response_json and len(response_json["choices"]) > 0:
        generated_text = response_json["choices"][0]["message"]["content"]
        return {"response": generated_text}
    else:
        return {"error": "No valid response content found"}


def prompt_response_handler(response_json):
    if "choices" in response_json and response_json["choices"]:
        return response_json["choices"][0]["text"].strip()
    elif "error" in response_json:
        return {"error": response_json["error"]}
    else:
        return {"error": "Unexpected response format"}


def embedding_response_handler(response_json):
    if "data" in response_json and len(response_json["data"]) > 0:
        return {"embedding": response_json["data"][0]["embedding"]}
    else:
        return {"error": "No valid embedding found"}


class LMStudioManager:
    """
    A manager class for interacting with LM Studio API.

    Common kwargs for API methods:
        model (str): The model to use for the request.
        messages (list): The messages to send in the request.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): Controls randomness in generation.
        top_p (float): Controls diversity via nucleus sampling.
        top_k (int): Controls diversity via top-k sampling.
        stream (bool): Whether to stream the response.
        stop (str or list): Sequences where the API will stop generating further tokens.
        price (float): The price for the request.
        presence_penalty (float): Penalizes new tokens based on their presence in the text so far.
        frequency_penalty (float): Penalizes new tokens based on their frequency in the text so far.
        logit_bias (dict): Adjusts the likelihood of specified tokens appearing in the completion.
        repeat_penalty (float): Penalizes repetition in generated text.
        seed (int): Sets the random seed for generation.
        prompt (str): The prompt to use for generation.
    """

    def __init__(self, base_url="http://localhost:1234"):
        self.base_url = base_url
        self.model_manager = LMStudioModelManager()

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

    def get_loaded_model_names(self):
        loaded_model_names = self.get_status_and_loaded_models()["models"]

        if not loaded_model_names:
            print(
                "No models are currently loaded. Please load a model in LM Studio and try again."
            )
            return

        return loaded_model_names

    def get_model_config_list(self, model_name):
        model_config = self.get_model_config(model_name)
        # print(f"Model config list: {model_config_list}")
        return {"config_list": model_config["config_list"]}

    def get_model_config(self, model_name):
        model_config = self.model_manager.get_model_config(model_name)

        if model_config is None:
            print(f"Failed to retrieve configuration for model: {model_name}")
            return None

        if "config_list" not in model_config:
            print(
                f"Invalid configuration for model: {model_name}. 'config_list' is missing."
            )
            return None

        return model_config

    def load_and_save_model_configs(self):
        models_and_status = self.get_status_and_loaded_models()

        if models_and_status["status"] == "error":
            print("LM Studio Error", models_and_status["message"])
            return []

        models = models_and_status["models"]

        if not models:
            print(
                "No models available. Please ensure LM Studio is running and has loaded models."
            )
            return []

        model_configs = [self.create_model_config(model) for model in models]
        self.save_model_library(model_configs)

        # config = self.get_model_config

        return models
        # return list(self.config_manager.get_available_model_configs())

    @handle_api_errors(prompt_response_handler)
    def send_prompt(self, prompt: str, model_config: dict, **kwargs: dict):
        """
        Send a prompt request to the LM Studio API.

        Args:
            prompt (str): The prompt to send.
            model_config (dict): The configuration for the model.
            **kwargs: Additional parameters as described in the class docstring.

        Returns:
            dict: The processed response from the API.
        """
        model_name = model_config['config_list'][0]['model']
        payload = self._prepare_payload(
            prompt=prompt,
            model=model_name,
            **kwargs
        )
        print(f"Sending payload: {payload} to {self.base_url}/v1/completions")
        return requests.post(f"{self.base_url}/v1/completions", json=payload)

    @handle_api_errors(chat_response_handler)
    def send_chat(self, messages, model_name, **kwargs):
        """
        Send a chat request to the LM Studio API.

        Args:
            messages (list): The messages to send in the request.
            model_name (str): The name of the model to use.
            **kwargs: Additional parameters as described in the class docstring.

        Returns:
            dict: The processed response from the API.
        """
        payload = self._prepare_payload(messages=messages, model=model_name, **kwargs)
        return requests.post(f"{self.base_url}/v1/chat/completions", json=payload)

    def _prepare_payload(self, **kwargs):
        """
        Prepare the payload for API requests.

        Args:
            **kwargs: Parameters to include in the payload.

        Returns:
            dict: The prepared payload.
        """
        payload = {
            "prompt": kwargs.get("prompt", ""),
            "model": kwargs.get("model", ""),
            "max_tokens": kwargs.get("max_tokens", 256),
            "temperature": kwargs.get("temperature", 0.7),
        }
        for param in VALID_LM_STUDIO_PARAMS:
            if param in kwargs and param not in payload:
                payload[param] = kwargs[param]
        return payload

    @handle_api_errors(embedding_response_handler)
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
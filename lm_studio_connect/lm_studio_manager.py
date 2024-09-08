# lm_studio_manager.py

"""
Module to manage interactions with LM Studio via API calls.
Handles model management and API responses.
"""
import functools
import json
from typing import Dict

import requests
from requests.exceptions import RequestException
from lm_studio_connect.utils.constants import VALID_LM_STUDIO_PARAMS
from lm_studio_connect.models.model_manager import LMStudioModelManager


def handle_api_errors(response_handler):
    """
    A decorator factory for handling API errors and processing responses.

    This decorator wraps API call functions to handle common exceptions and
    process the API response using the provided response handler.

    Args:
        response_handler (callable):
        A function to process the successful API response.

    Returns:
        callable: A decorator function.
    """

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
    """
    Process the JSON response from a chat API call.

    Args:
        response_json (dict): The JSON response from the API.

    Returns:
        dict: A dictionary containing either the
        generated text response or an error message.
    """
    if "choices" in response_json and len(response_json["choices"]) > 0:
        generated_text = response_json["choices"][0]["message"]["content"]
        return {"response": generated_text}

    return {"error": "No valid response content found"}


def prompt_response_handler(response_json):
    """
    Process the JSON response from a prompt-based API call.

    Args:
        response_json (dict): The JSON response from the API.

    Returns:
        str or dict: The generated text if successful,
        or a dictionary with an error message.
    """
    if "choices" in response_json and response_json["choices"]:
        return response_json["choices"][0]["text"].strip()
    if "error" in response_json:
        return {"error": response_json["error"]}

    return {"error": "Unexpected response format"}


def embedding_response_handler(response_json):
    """
    Process the JSON response from an embedding API call.

    Args:
        response_json (dict): The JSON response from the API.

    Returns:
        dict: A dictionary containing either the embedding or an error message.
    """
    if "data" in response_json and len(response_json["data"]) > 0:
        return {"embedding": response_json["data"][0]["embedding"]}

    return {"error": "No valid embedding found"}


class LMStudioManager:
    """
    A manager class for interacting with LM Studio API.

    This class provides methods to interact with LM Studio, check its status,
    and manage loaded models.

    Attributes:
        base_url (str): The base URL for the LM Studio API.
        model_manager (LMStudioModelManager):
            An instance of LMStudioModelManager
            for handling model-specific operations.

    Common kwargs for API methods:
        model (str): The model to use for the request.
        messages (list): The messages to send in the request.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): Controls randomness in generation.
        top_p (float): Controls diversity via nucleus sampling.
        top_k (int): Controls diversity via top-k sampling.
        stream (bool): Whether to stream the response.
        stop (str or list): Sequences where the API will
        stop generating further tokens.
        price (float): The price for the request.
        presence_penalty (float): Penalizes new tokens
        based on their presence in the text so far.
        frequency_penalty (float): Penalizes new tokens
        based on their frequency in the text so far.
        logit_bias (dict): Adjusts the likelihood of
        specified tokens appearing in the completion.
        repeat_penalty (float): Penalizes repetition in generated text.
        seed (int): Sets the random seed for generation.
        prompt (str): The prompt to use for generation.
    """

    def __init__(self, base_url="http://localhost:1234"):
        """
        Initialize the LMStudioManager.

        Args:
            base_url (str, optional): The base URL for the LM Studio API.
                                      Defaults to "http://localhost:1234".
        """
        self.base_url = base_url
        self.model_manager = LMStudioModelManager()

    def get_status_and_loaded_models(self):
        """
        Retrieve the status of LM Studio and the list of loaded models.

        Returns:
            dict: A dictionary containing the status of
            LM Studio and the list of loaded models.
                  Possible statuses are "active", "idle", or "error".
        """
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=10000)
            response.raise_for_status()
            loaded_models = response.json()["data"]
            return (
                {"status": "active", "models": [model["id"] for model in loaded_models]}
                if loaded_models
                else {"status": "idle", "models": []}
            )
        except RequestException as e:
            return {"status": "error", "message": str(e)}

    def custom_llm_studio_api_call(self):
        """
        Make a custom API call to the LM Studio base URL.

        Returns:
            dict: The JSON response from the API call,
            or an error status if the call fails.
        """
        try:
            response = requests.get(f"{self.base_url}", timeout=90000)
            return response.json()
        except RequestException as e:
            return {"status": "error", "message": str(e)}

    def is_lm_studio_active(self):
        """
        Check if LM Studio is active.

        Returns:
            bool: True if LM Studio is active, False otherwise.
        """
        return self.get_status_and_loaded_models()["status"] == "active"

    def is_model_loaded(self, model):
        """
        Check if a specific model is loaded in LM Studio.

        Args:
            model (str): The name of the model to check.

        Returns:
            bool: True if the model is loaded, False otherwise.
        """
        models_statuses = self.get_status_and_loaded_models()["models"]
        return any(model in m for m in models_statuses)

    def get_loaded_model_names(self):
        """
        Get the names of all currently loaded models in LM Studio.

        Returns:
            list: A list of loaded model names, or None if no models are loaded.
        """
        loaded_model_names = self.get_status_and_loaded_models()["models"]

        if not loaded_model_names:
            print(
                """No models are currently loaded. 
                Please load a model in LM Studio and try again."""
            )

        return loaded_model_names

    def get_model_config_list(self, model_name):
        """
        Retrieve the configuration list for a specific model.

        This method extracts the 'config_list' from the model's configuration.

        Args:
            model_name (str): The name of the model to retrieve the configuration for.

        Returns:
            dict: A dictionary containing the 'config_list' for the specified model.
        """
        model_config = self.get_model_config(model_name)
        return {"config_list": model_config["config_list"]}

    def get_model_config(self, model_name):
        """
        Retrieve the full configuration for a specific model.

        This method attempts to get the model configuration from the model manager.
        It performs validity checks on the retrieved configuration.

        Args:
            model_name (str): The name of the model to retrieve the configuration for.

        Returns:
            dict: The full configuration for the specified model if valid, None otherwise.
        """
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
        """
        Load configurations for all available models and save them.

        This method retrieves the status and list of loaded models from LM Studio,
        creates configurations for each model, and saves them to the model library.

        Returns:
            list: A list of model names for which configurations were loaded and saved.
                  Returns an empty list if no models are available or if an error occurs.
        """
        models_and_status = self.get_status_and_loaded_models()

        if models_and_status["status"] == "error":
            print("LM Studio Error", models_and_status["message"])
            return []

        models = models_and_status["models"]

        if not models:
            print(
                """No models available. Please ensure 
                LM Studio is running and has loaded models."""
            )
            return []

        model_configs = [
            self.model_manager.create_model_config(model) for model in models
        ]
        self.model_manager.save_model_library(model_configs)

        return models

    @handle_api_errors(prompt_response_handler)
    def send_prompt(self, prompt: str, model_name: str, **kwargs: Dict):
        """
        Send a prompt request to the LM Studio API.

        Args:
            prompt (str): The prompt to send.
            model_config (dict): The configuration for the model.
            **kwargs: Additional parameters as described in the class docstring.

        Returns:
            dict: The processed response from the API.
        """
        payload = self._prepare_payload(prompt=prompt, model=model_name, **kwargs)
        print(f"Sending payload: {payload} to {self.base_url}/v1/completions")
        return requests.post(
            f"{self.base_url}/v1/completions", json=payload, timeout=60000
        )

    @handle_api_errors(chat_response_handler)
    def send_chat(self, messages, model_name: str, **kwargs: Dict):
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
        return requests.post(
            f"{self.base_url}/v1/chat/completions", json=payload, timeout=60000
        )

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
        """
        Generate an embedding for the given input text using the specified model.

        This method sends a POST request to the LM Studio API to generate an embedding
        for the provided input text using the specified model. It uses the
        `handle_api_errors` decorator to manage API errors and process the response.

        Args:
            input_text (str): The text to generate an embedding for.
            model_name (str): The name of the model to use for generating the embedding.

        Returns:
            dict: A dictionary containing either the generated embedding or an error message.
                  The structure of the return value is
                  determined by the `embedding_response_handler`.

        Raises:
            RequestException: If there's an error in making the API request.
                              This exception is caught and converted to an error dictionary.

        Note:
            This method is decorated with `@handle_api_errors(embedding_response_handler)`,
            which processes the API response and handles potential errors.
        """
        try:
            response = requests.post(
                f"{self.base_url}/v1/embeddings",
                json={"input": input_text, "model": model_name},
                timeout=60000,
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            return {"error": f"An error occurred: {e}"}

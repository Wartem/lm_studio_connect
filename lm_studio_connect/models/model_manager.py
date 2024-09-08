# model_manager.py

"""
Module for managing model configurations in LM Studio.
Handles creating, loading, and saving of models.
"""

import os
from ..config.config_manager import ConfigManager
from ..utils.helpers import get_short_name
from ..utils.constants import VALID_LM_STUDIO_PARAMS


class LMStudioModelManager:
    """
    Manages model configurations for LM Studio.

    This class handles the creation, loading, and saving of model configurations
    for use with LM Studio. It interacts with a configuration file to store and
    retrieve model settings.

    Attributes:
        config_manager (ConfigManager): An instance of ConfigManager for handling
                                        configuration file operations.
    """

    def __init__(self, config_file=None):
        """
        Initialize the LMStudioModelManager.

        Args:
            config_file (str, optional): Path to the configuration file. If not provided,
                                         a default path will be used.
        """
        config_file = (
            config_file
            if config_file
            else os.path.join(os.path.dirname(__file__), "../config/model_library.json")
        )

        self.config_manager = ConfigManager(config_file)

    def get_default_config(self, model_name):
        """
        Returns the default configuration for connecting to LM Studio.

        Args:
            model_name (str): The name of the model to be used in LM Studio.

        Returns:
            dict: A dictionary containing the configuration for LM Studio connection.
                It includes a 'config_list' with model details, base URL, and API key.
        """
        return {
            "config_list": [
                {
                    "model": model_name,
                    "base_url": "http://localhost:1234/v1",
                    "api_key": "lm-studio",
                }
            ]
        }

    def create_model_config(self, model_name, **kwargs):
        """
        Create a configuration for a given model.

        Args:
            model_name (str): The name of the model.
            **kwargs: Additional configuration parameters.

        Returns:
            dict: A dictionary containing the model configuration.
        """
        # Default values
        config = self.get_default_config(model_name)

        # Only add parameters to config if they are valid
        for param, value in kwargs.items():
            if param in VALID_LM_STUDIO_PARAMS:
                config[param] = value

        return {
            get_short_name(model_name): {
                "config_list": [config],
                "cache_seed": kwargs.get("cache_seed", None),
                "max_tokens": kwargs.get(
                    "max_tokens", 1024
                ),  # Default max_tokens if not provided
            }
        }

    def save_model_library(self, model_configs):
        """
        Save model configurations to the model library.

        This method updates the existing model library with new configurations,
        adding new models if they don't exist and updating existing ones.

        Args:
            model_configs (list): A list of model configurations to save.
        """
        existing_data = self.config_manager.load_model_configs()

        for config in model_configs:
            for key, value in config.items():
                if key not in existing_data:
                    existing_data[key] = value

        self.config_manager.save_model_configs(existing_data)

    def get_model_config(self, model_name: str) -> dict:
        """
        Retrieve the configuration for a specific model.

        This method attempts to find the configuration using both the full model name
        and a shortened version. If no configuration is found, it returns a default configuration.

        Args:
            model_name (str): The name of the model to retrieve the configuration for.

        Returns:
            dict: The configuration for the specified model,
            or a default configuration if not found.
        """
        configs = self.config_manager.load_model_configs()

        # Try to get config using the full model name
        config = configs.get(model_name)

        if config is None:
            # If not found, try with the short name
            short_name = get_short_name(model_name)
            config = configs.get(short_name)

        if config is None:
            print(f"Warning: Configuration for model '{model_name}' not found.")
            return self.get_default_config(model_name)

        return config

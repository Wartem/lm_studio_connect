import os
import random
from lm_studio_connect.config.config_manager import (
    ConfigManager,
)
from lm_studio_connect.utils.helpers import get_short_name
from lm_studio_connect.utils.constants import VALID_LM_STUDIO_PARAMS


class LMStudioModelManager:
    def __init__(self, config_file=None):
        config_file = (
            config_file
            if config_file
            else os.path.join(os.path.dirname(__file__), "../config/model_library.json")
        )

        self.config_manager = ConfigManager(config_file)

    def create_model_config(self, model_name, **kwargs):
        # Default values
        config = {
            "model": model_name,
            "base_url": self.lm_manager.base_url,
            "api_key": "lm-studio",
        }

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
        existing_data = self.config_manager.load_model_configs()

        for config in model_configs:
            for key, value in config.items():
                if key not in existing_data:
                    existing_data[key] = value

        self.config_manager.save_model_configs(existing_data)

    def get_model_config(self, model_name: str) -> dict:
        configs = self.config_manager.load_model_configs()

        # Try to get config using the full model name
        config = configs.get(model_name)

        if config is None:
            # If not found, try with the short name
            short_name = get_short_name(model_name)
            config = configs.get(short_name)

        if config is None:
            print(f"Warning: Configuration for model '{model_name}' not found.")
            return {
                "config_list": [
                    {
                        "model": model_name,
                        "base_url": "http://localhost:1234/v1",
                        "api_key": "lm-studio",
                    }
                ]
            }

        return config

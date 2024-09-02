from config.config_manager import ConfigManager
from lm_studio_connection.lm_studio_manager import LMStudioManager
from utils.helpers import get_short_name
from utils.constants import VALID_LM_STUDIO_PARAMS

class ModelManager:
    def __init__(self, config_file):
        self.config_manager = ConfigManager(config_file)
        self.lm_manager = LMStudioManager()

    def load_and_save_models(self):
        models_and_status = self.lm_manager.get_status_and_loaded_models()
        
        if models_and_status["status"] == "error":
            print("LM Studio Error", models_and_status["message"])
            return []
        
        models = models_and_status["models"]
        
        if not models:
            print("No models available. Please ensure LM Studio is running and has loaded models.")
            return []
        
        model_configs = [self.create_model_config(model) for model in models]
        self.save_model_library(model_configs)
        
        return models
    
    
    def create_model_config(self, model_name, **kwargs):
        # Default values
        config = {
            "model": model_name,
            "base_url": self.lm_manager.base_url,
            "api_key": "lm-studio",
        }

        # Only add parameters to config if they are provided and valid
        for param in VALID_LM_STUDIO_PARAMS:
            if param in kwargs:
                config[param] = kwargs[param]

        return {
            get_short_name(model_name): {
                "config_list": [config],
                "cache_seed": kwargs.get("cache_seed", None),
                "max_tokens": kwargs.get("max_tokens", 1024)  # Default max_tokens if not provided
            }
        }

    def save_model_library(self, model_configs):
        existing_data = self.config_manager.model_configs

        for config in model_configs:
            for key, value in config.items():
                if key not in existing_data:
                    existing_data[key] = value

        self.config_manager.save_model_configs()
        
    def get_model_config(self, model_name):
        return self.config_manager.get_model_config(model_name)

'''
    def add_model_to_library(self, name, model_config):
        if name in self.config_manager.model_configs:
            print(f"Model {name} already exists. Skipping addition.")
        else:
            self.config_manager.update_model_config(name, model_config)
'''
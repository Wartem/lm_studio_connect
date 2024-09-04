import json
import functools


def handle_config_errors(default_config=None):
    if default_config is None:
        default_config = {}

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if not result:
                    print("Warning: The configuration file is empty.")
                    return default_config
                return result
            except json.JSONDecodeError:
                print("Error: The configuration file is not valid JSON or is completely empty.")
                return default_config
            except FileNotFoundError:
                print(f"Error: The configuration file was not found.")
                return default_config
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
                return default_config
        return wrapper
    return decorator

def handle_config_operations(operation_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                print(f"Successfully {operation_type} the configuration.")
                return result
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON data for {operation_type}.")
            except FileNotFoundError:
                print(f"Error: The configuration file was not found.")
            except PermissionError:
                print(f"Error: Permission denied. Unable to {operation_type} the configuration file.")
            except IOError as e:
                print(f"Error: An I/O error occurred while trying to {operation_type} the configuration: {str(e)}")
            except Exception as e:
                print(f"An unexpected error occurred while trying to {operation_type} the configuration: {str(e)}")
            return None
        return wrapper
    return decorator

class ConfigManager:
    def __init__(self, config_file="model_library.json"):
        self.config_file = config_file

    def get_available_model_names(self):
        return list(self.load_model_configs().keys())

    def get_available_model_configs(self):
        return list(self.load_model_configs())

    def get_model_config(self, model_name):
        return self.load_model_configs().get(model_name)

    """
    def update_model_config(self, model_name, config):
        self.model_configs[model_name] = config
        self.save_model_configs()
    """
    
    @handle_config_errors()
    def load_model_configs(self):
        with open(self.config_file, "r") as f:
            return json.load(f)

    @handle_config_operations("save")
    def save_model_configs(self, configs):
        with open(self.config_file, "w") as f:
            json.dump(configs, f, indent=4)

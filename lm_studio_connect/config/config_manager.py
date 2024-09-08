# config_manager.py

"""
Module for managing configuration files in LM Studio.
Includes functions for loading, saving, and error handling of configs.
"""

import json
import functools
from typing import Optional, Dict, Callable, Any


def handle_config_errors(default_config: Optional[Dict] = None):
    """
    A decorator factory that adds error handling for configuration loading operations.

    Args:
        default_config (Optional[Dict]):
            A default configuration to use if errors occur.
            If None, an empty dictionary will be used.

    Returns:
        Callable: A decorator that wraps a function with error handling.
    """
    if default_config is None:
        default_config = {}

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Dict:
            try:
                result = func(*args, **kwargs)
                if not result:
                    print("Warning: The configuration file is empty.")
                    return default_config
                return result
            except json.JSONDecodeError:
                print(
                    """Error: The configuration file is 
                    not valid JSON or is completely empty."""
                )
                return default_config
            except FileNotFoundError:
                print("Error: The configuration file was not found.")
                return default_config
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
                return default_config

        return wrapper

    return decorator


def handle_config_operations(operation_type: str):
    """
    A decorator factory that adds error handling for configuration operations.

    Args:
        operation_type (str): The type of operation being performed
        (e.g., 'load', 'save').

    Returns:
        A decorator that wraps a function with error handling.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                print(f"""Successfully {operation_type} the configuration.""")
                return result
            except json.JSONDecodeError:
                print(f"""Error: Invalid JSON data for {operation_type}.""")
            except FileNotFoundError:
                print("""Error: The configuration file was not found.""")
            except PermissionError:
                print(
                    f"""Error: Permission denied. Unable to 
                    {operation_type} the configuration file."""
                )
            except IOError as e:
                print(
                    f"""Error: An I/O error occurred while trying to 
                    {operation_type} the configuration: {str(e)}"""
                )
            except Exception as e:
                print(
                    f"""An unexpected error occurred while trying to 
                    {operation_type} the configuration: {str(e)}"""
                )
            return None

        return wrapper

    return decorator


class ConfigManager:
    """
    A manager class for handling configuration files related to model management.

    This class provides methods for loading and saving model configurations.
    """

    def __init__(self, config_file="model_library.json"):
        """
        Initialize the ConfigManager with the provided config file.

        Args:
            config_file (str): Path to the configuration file. Defaults to 'model_library.json'.
        """
        self.config_file = config_file

    def load_available_model_names(self):
        """
        Returns a list of available model names.
        """
        return list(self.load_model_configs().keys())

    def load_available_model_configs(self):
        """
        Returns a list of available model configurations.
        """
        return list(self.load_model_configs())

    def load_model_config(self, model_name) -> dict:
        """
        Returns the configuration for a specific model.

        Args:
            model_name (str): The name of the model.

        Returns:
            dict: The configuration of the specified model.
        """
        return self.load_model_configs().get(model_name)

    @handle_config_errors()
    # Decorates the load_model_configs method, providing a default configuration
    # and handling potential errors that may occur during loading.
    def load_model_configs(self) -> dict:
        """Load model configurations from the specified JSON file.
        Handles common errors like missing or invalid files.

        Returns:
            dict: A dictionary containing the loaded model configuration data,
            with keys as model names and values as their respective configurations.

        Raises:
            FileNotFoundError: If the configuration file does
            not exist in the specified location.
            json.JSONDecodeError: If the configuration
            file is not a valid JSON string or if it's empty.
            Exception: For any unexpected errors during loading.
        """

        with open(self.config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    @handle_config_operations("save")
    def save_model_configs(self, configs: str):
        """Saves the configuration data to the specified model library file.

        This method accepts an argument 'configs', which should be a dictionary
        containing the model configurations. The function attempts
        to write these configurations as JSON-formatted text into the specified
        'model_library.json' file, ensuring it is properly formatted
        with indentation for readability.

        Args:
            configs (dict): A dictionary containing model configurations.

        Raises:
            IOError: If there are any issues writing to the
            specified configuration file due to I/O errors.
        """
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(configs, f, indent=4)

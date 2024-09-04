import sys
import os
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lm_studio_connect.models.model_manager import ModelManager


def send_prompt(prompt="Tell me about something advanced and interesting about Python"):
    model_manager = ModelManager()

    # Load and get available models
    available_models = model_manager.load_and_save_model_configs()

    if not available_models:
        print("No models available")
        return

    selected_model_name = random.choice(available_models)
    selected_model_config = model_manager.get_model_config(selected_model_name)

    print(f"Selected model: {selected_model_name}")
    print(f"Using config: {selected_model_config}")

    response = model_manager.lm_manager.send_prompt(
        prompt=prompt, model_config=selected_model_config
    )

    if "choices" in response and response["choices"]:
        print("Response:", response["choices"][0]["text"].strip())
    else:
        print("No valid response received.")


if __name__ == "__main__":
    send_prompt()

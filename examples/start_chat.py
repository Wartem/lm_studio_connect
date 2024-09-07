import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lm_studio_connect.lm_studio_manager import LMStudioManager
from lm_studio_connect.models.model_selector import select_model_name


def start_chat():
    lm_studio_manager = LMStudioManager()
    loaded_model_names = lm_studio_manager.get_loaded_model_names()
    selected_model_name = select_model_name(loaded_model_names)
    model_config = lm_studio_manager.get_model_config(selected_model_name)

    response = lm_studio_manager.send_chat(
        model_name=selected_model_name,
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "How do I init and update a git submodule?"},
        ],
        temperature=0.7,
        max_tokens=-1,
        # stream = True,
        model_config={"config_list": model_config["config_list"]},
    )

    print("response", response)


if __name__ == "__main__":
    start_chat()

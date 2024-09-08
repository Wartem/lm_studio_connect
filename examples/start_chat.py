from lm_studio_connect.lm_studio_manager import LMStudioManager
from lm_studio_connect.models.model_selector import select_model_name


def start_chat():
    lm_studio_manager = LMStudioManager()
    loaded_model_names = lm_studio_manager.get_loaded_model_names()
    selected_model_name = select_model_name(loaded_model_names)

    response = lm_studio_manager.send_chat(
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "How do I init and update a git submodule?"},
        ],
        model_name=selected_model_name,
        temperature=0.7,
        max_tokens=-1,
    )

    print("response", response)


if __name__ == "__main__":
    start_chat()

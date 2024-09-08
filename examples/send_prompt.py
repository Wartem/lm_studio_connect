from lm_studio_connect.lm_studio_manager import LMStudioManager
from lm_studio_connect.models.model_selector import select_model_name


def send_prompt():
    lm_studio_manager = LMStudioManager()
    loaded_model_names = lm_studio_manager.get_loaded_model_names()
    selected_model_name = select_model_name(loaded_model_names)

    response = lm_studio_manager.send_prompt(
        prompt="Tell me about something advanced and interesting about Python",
        model_name=selected_model_name,
        max_tokens=1024,
    )

    print("response", response)


if __name__ == "__main__":
    send_prompt()

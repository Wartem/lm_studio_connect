import sys
import os
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from lm_studio_connect.models.model_manager import ModelManager
import autogen


def start_autogen_conversation(
    initial_message="""
                               Let's discuss Open-Source Programming Frameworks 
                               for Agentic AI, and how to use them!
                               """,
):

    model_manager = ModelManager()
    available_models = model_manager.load_and_save_model_configs()

    if not available_models:
        print("No models available.")
        return

    selected_model = random.choice(available_models)
    model_config = model_manager.get_model_config(selected_model)

    print(f"Selected model: {selected_model}")
    print(f"Model config: {model_config}")

    steven = autogen.ConversableAgent(
        "Steven",
        llm_config={"config_list": model_config["config_list"]},
        system_message="""
        Your name is Steven and you are an expert in Agentic AI.
        """,
    )

    user_proxy = autogen.UserProxyAgent(
        "user_proxy",
        llm_config={"config_list": model_config["config_list"]},
    )

    user_proxy.initiate_chat(steven, message=initial_message)


if __name__ == "__main__":
    start_autogen_conversation()

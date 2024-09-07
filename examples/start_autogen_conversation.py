import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import autogen
from lm_studio_connect.lm_studio_manager import LMStudioManager
from lm_studio_connect.models.model_selector import select_model_name


def main():
    lm_studio_manager = LMStudioManager()
    loaded_model_names = lm_studio_manager.get_loaded_model_names()
    selected_model_name = select_model_name(loaded_model_names)
    model_config_list = lm_studio_manager.get_model_config_list(selected_model_name)

    start_autogen_conversation(model_config_list)


def start_autogen_conversation(
    model_config_list,
    initial_message="""
                    Let's discuss Open-Source Programming Frameworks 
                    for Agentic AI, and how to use them!
                    """,
                    ):

    steven = autogen.ConversableAgent(
        "Steven",
        system_message="""
        Your name is Steven and you are an expert in Agentic AI.
        """,
        llm_config=model_config_list,
    )

    user_proxy = autogen.UserProxyAgent(
        "user_proxy",
        llm_config=model_config_list,
    )

    user_proxy.initiate_chat(steven, message=initial_message)


if __name__ == "__main__":
    main()

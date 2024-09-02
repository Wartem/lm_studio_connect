import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lm_studio_connect.models.model_manager import ModelManager
import autogen

def start_autogen_conversation(initial_message='''
                               Let's discuss Open-Source Programming Frameworks 
                               for Agentic AI, and how to use them!
                               '''):
    
    model_manager = ModelManager()
    model = model_manager.load_and_save_models().pop()
    
    if not model:
        print("No models available.")
        return
        
    phil = autogen.ConversableAgent(
        "Steven",
        llm_config=model_manager.get_model_config(model),
        system_message="""
        Your name is Steven and you are an expert in Agentic AI.
        """,
    )

    user_proxy = autogen.UserProxyAgent(
        "user_proxy",
        llm_config=model_manager.get_model_config(model),
    )

    user_proxy.initiate_chat(phil, message=initial_message)
    

if __name__ == "__main__":
    start_autogen_conversation()
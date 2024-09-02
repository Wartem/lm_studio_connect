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
    
    available_models = model_manager.load_and_save_models()
    model = available_models.pop()
        
    phil = autogen.ConversableAgent(
        "Phil",
        llm_config=model_manager.get_model_config(model),
        system_message="""
        Your name is Phil and you are a comedian.
        """,
    )

    user_proxy = autogen.UserProxyAgent(
        "user_proxy",
    )

    user_proxy.initiate_chat(phil, message=initial_message)
    

if __name__ == "__main__":
    start_autogen_conversation()
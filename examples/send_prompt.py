import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lm_studio_connect.models.model_manager import ModelManager

def send_prompt(prompt="Tell me about something advanced and interesting about Python"):
    model_manager = ModelManager()

    # Load and get available models
    available_models = model_manager.load_and_save_models()
    
    if not available_models:
        return

    selected_model = random.choice(available_models)
    print(f"Selected model: {selected_model}")

    response = model_manager.lm_manager.send_prompt(prompt=prompt, model_name=selected_model)

    if 'choices' in response and response['choices']:
        print("Response:", response['choices'][0]['text'].strip())
    else:
        print("No valid response received.")
        
        

if __name__ == "__main__":
    send_prompt()
from models.model_manager import ModelManager
import random
import autogen

def send_prompt(prompt):
    model_manager = ModelManager("model_library.json")

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

        
def start_autogen_conversation():
    model_manager = ModelManager("model_library.json")
    
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

    user_proxy.initiate_chat(phil, message="Tell me a joke!")

    
    
def display_menu():
    menu_options = [
        "\n-- LM Studio Connection Examples --",
        "1. Send a prompt to LLM",
        "2. Start an Autogen Conversation",
        "3. Exit",
        "----------------"
    ]
    print("\n".join(menu_options))


def get_user_choice():
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice in ["1", "2", "3"]:
            return int(choice)
        else:
            print("Invalid input. Please enter a number between 1 and 3.")

def main():
    while True:
        display_menu()
        user_choice = get_user_choice()

        if user_choice == 1:
            send_prompt("Explain the concept of machine learning in one sentence.")
        elif user_choice == 2:
            start_autogen_conversation()
        elif user_choice == 3:
            print("Exiting the program. Goodbye!")
            break

        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main()
    
    
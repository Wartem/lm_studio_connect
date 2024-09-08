![Python](https://img.shields.io/badge/language-Python-blue.svg)
![LM-Studio](https://img.shields.io/badge/LLM-LM--Studio-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-0.1.0-brightgreen.svg)
![AI](https://img.shields.io/badge/AI-enabled-blue.svg)
![AutoGen](https://img.shields.io/badge/framework-AutoGen-orange.svg)
![Local LLM](https://img.shields.io/badge/LLM-Local-red.svg)

# LLM Studio Integration and Model Management

## Overview
This repository provides a simple framework for integrating and managing language models using a local LLM (Language Model) Studio instance. 
It includes scripts for managing model configurations, sending prompts, and starting automated conversations using preloaded models. 
The project is designed to streamline the process of interacting with LLMs, allowing for seamless model management and interaction.
------------
## Example of usage, with LM Studio running in the background

```
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
        model_config={"config_list": model_config["config_list"]},
    )

    print("response", response)
```
## Example 2 of usage, using Autogen and LM Studio running in the background
```
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

```

## Project Structure

- **`config/` Directory**:
  - **`config_manager.py`**: Manages the loading, retrieval, and saving of model configurations stored in `model_library.json`. This module ensures that the system can easily retrieve and update model configurations as needed.

- **`lm_studio_connection/` Directory**:
  - **`lm_studio_manager.py`**: Handles communication with the LLM Studio API. It includes methods for checking the status of the LLM Studio, loading models, sending prompts, and generating embeddings. This module is crucial for interacting with the LLM models hosted on the local LLM Studio instance.

- **`models/` Directory**:
  - **`model_manager.py`**: Manages the loading, saving, and configuration of models using the LLM Studio. It works closely with `lm_studio_manager.py` and `config_manager.py` to provide a streamlined interface for managing the models available in the LLM Studio.

- **`utils/` Directory**:
  - **`constants.py`**: Defines constants used throughout the project, such as valid LLM Studio parameters.
  - **`helpers.py`**: Contains utility functions, such as `get_short_name`, which extracts the short name of a model from its full path or name.

## Key Features

- **Model Interaction**: Send prompts to LLM models and receive responses directly through the console interface.
- **Autogen Conversations**: Start and manage conversations with a pre-defined conversational agent, allowing for the creation of interactive AI experiences.
- **Model Management**: Automatically load, save, and configure models, simplifying the process of integrating multiple language models into your workflow.
- **Utility Scripts**: Includes scripts for printing directory structures and managing configuration files, aiding in project organization and documentation.

## Requirements

- Python 3.8+
- LM Studio (with models loaded)
- Dependencies specified in `requirements.txt` 

- Autogen library
Autogen is included solely as an example for usage and integration with LLM Studio and is not otherwise a component of this project.

## Installation

Clone the repository:
```
git clone https://github.com/yourusername/lm_studio_connect.git
cd lm_studio_connect
```

### Optional: Create a virtual environment
```
python -m venv venv
```
***Activate the virtual environment***

On Windows:
```
venv\Scripts\activate
```

On macOS and Linux:
```
source venv/bin/activate
```

## How to Use

1. **Run** the examples inside the folder examples.
2. **Modify `model_library.json`**: Add or adjust model configurations as needed to work with different LLMs.
3. **Use `structure_print.py`**: Generate a directory structure report to document the project setup.

## Disclaimer

**LM Studio Connect** is an independent project and has no affiliation with the official LM Studio team or its original codebase.

- This project is developed as a separate initiative to provide enhanced connectivity options for local language models.
- It is not endorsed, supported, or maintained by the official LM Studio team.
- Any issues, features, or updates related to LM Studio Connect are separate from the official LM Studio project.

> **Note**: For official support, documentation, and updates regarding LM Studio itself, please refer to the [official LM Studio resources](https://lmstudio.ai).

## License

This project is licensed under the MIT License.

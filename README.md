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

## Project Structure

- **Root Directory**:
  - **`main.py`**: A script with examples of how to interact with the LLM Studio with the help of this project. It provides a user interface for sending prompts to loaded models, initiating automated conversations with a conversational agent, and managing the overall workflow.
  - **`model_library.json`**: A JSON file storing configurations for various models available in the LLM Studio. It contains details such as model names, API endpoints, temperature settings, and token limits.

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

## How to Use

1. **Run `main.py`**: This will launch the main interface, where you can select options to interact with the models or start a conversation.
2. **Modify `model_library.json`**: Add or adjust model configurations as needed to work with different LLMs.
3. **Use `structure_print.py`**: Generate a directory structure report to document the project setup.

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
### Activate the virtual environment

On Windows:
```
venv\Scripts\activate
```

On macOS and Linux:
```
source venv/bin/activate
```

## License

This project is licensed under the MIT License.

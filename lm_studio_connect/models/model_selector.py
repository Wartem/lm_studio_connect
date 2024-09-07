from enum import Enum
import random
from typing import Optional, Set, Dict


class SelectionMode(Enum):
    DEFAULT = "default"
    SPECIFIC = "specific"
    RANDOM = "random"
    CHOOSE = "choose"


def select_model_name(
    available_models: Dict,
    mode: SelectionMode = SelectionMode.DEFAULT,
    name: Optional[str] = None,
) -> str:
    """
    Select a model name based on the specified mode.

    Args:
        mode (SelectionMode): The selection mode to use. Defaults to SelectionMode.DEFAULT.
        name (Optional[str]): The name of a specific model to select. Only used when mode is SelectionMode.SPECIFIC.

    Returns:
        str: The selected model name.

    Raises:
        ValueError: If the mode is invalid, if no models are available, or if a specific model name is not found.

    Usage:
        selector = ModelSelector()

        # Default mode (returns the first available model)
        model = selector.get_model_name()

        # Specific model selection
        model = selector.get_model_name(mode=SelectionMode.SPECIFIC, name="gpt-3.5-turbo")

        # Random selection
        model = selector.get_model_name(mode=SelectionMode.RANDOM)

        # Interactive choice
        model = selector.get_model_name(mode=SelectionMode.CHOOSE)
    """

    if not available_models:
        raise ValueError("No models available")

    selection_methods = {
        SelectionMode.DEFAULT: lambda: next(iter(available_models)),
        SelectionMode.SPECIFIC: lambda: name if name in available_models else None,
        SelectionMode.RANDOM: lambda: random.choice(list(available_models)),
        SelectionMode.CHOOSE: lambda: interactive_choice(available_models),
    }

    selected_model = selection_methods.get(
        mode, selection_methods[SelectionMode.DEFAULT]
    )()

    if selected_model is None:
        raise ValueError(f"Invalid mode or model name not found")

    # print(f"Selected model: {selected_model}")

    return selected_model


def interactive_choice(models: Set[str]) -> str:
    """
    Prompt the user to choose a model interactively.

    Args:
        models (Set[str]): Set of available model names.

    Returns:
        str: The chosen model name.
    """
    print("Available models:")
    model_list = list(models)
    # for i, model in enumerate(model_list, 1):
    # print(f"{i}. {model}")

    while True:
        try:
            choice = int(input("Enter the number of your chosen model: "))
            if 1 <= choice <= len(model_list):
                return model_list[choice - 1]
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

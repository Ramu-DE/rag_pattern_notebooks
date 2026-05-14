"""
Environment Loader for RAG Techniques Notebooks
Loads environment variables from the centralized .env file
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables from the centralized .env file.
    Searches for .env file in the project root directory.

    Returns:
        bool: True if .env file was found and loaded, False otherwise
    """
    # Get the current notebook's directory
    current_dir = Path.cwd()

    # Search for .env file in parent directories (up to 3 levels)
    env_file = None
    search_dir = current_dir

    for _ in range(4):
        potential_env = search_dir / '.env'
        if potential_env.exists():
            env_file = potential_env
            break
        search_dir = search_dir.parent

    if env_file and env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Environment loaded from: {env_file}")
        return True
    else:
        print("⚠️  Warning: .env file not found!")
        print("Please create a .env file in the project root with your API keys.")
        return False

def get_env_variable(var_name, default=None, required=False):
    """
    Get an environment variable with optional default and required check.

    Args:
        var_name (str): Name of the environment variable
        default: Default value if variable is not set
        required (bool): If True, raises error if variable is not set

    Returns:
        str: Value of the environment variable

    Raises:
        ValueError: If required=True and variable is not set
    """
    value = os.getenv(var_name, default)

    if required and not value:
        raise ValueError(f"Required environment variable '{var_name}' is not set!")

    return value

def check_required_keys(*keys):
    """
    Check if required API keys are set in environment.

    Args:
        *keys: Variable number of environment variable names to check

    Returns:
        dict: Dictionary with key names and their status (True/False)
    """
    status = {}
    all_present = True

    print("🔍 Checking required API keys...")
    for key in keys:
        value = os.getenv(key)
        is_set = bool(value and value.strip() and value != "")
        status[key] = is_set

        if is_set:
            print(f"  ✅ {key}: Set")
        else:
            print(f"  ❌ {key}: Not set")
            all_present = False

    if all_present:
        print("\n✅ All required API keys are configured!")
    else:
        print("\n⚠️  Some API keys are missing. Please update your .env file.")

    return status

def display_config():
    """
    Display current configuration (without showing sensitive values)
    """
    print("=" * 60)
    print("Current RAG Techniques Configuration")
    print("=" * 60)

    configs = {
        "Vector DB Provider": os.getenv('VECTOR_DB_PROVIDER', 'Not set'),
        "Default LLM Model": os.getenv('DEFAULT_LLM_MODEL', 'Not set'),
        "Default Embedding Model": os.getenv('DEFAULT_EMBEDDING_MODEL', 'Not set'),
        "Temperature": os.getenv('DEFAULT_TEMPERATURE', 'Not set'),
        "Data Directory": os.getenv('DATA_DIR', 'Not set'),
        "LangChain Tracing": os.getenv('LANGCHAIN_TRACING_V2', 'Not set'),
    }

    for key, value in configs.items():
        print(f"{key:.<30} {value}")

    print("=" * 60)

if __name__ == "__main__":
    # Test the environment loader
    load_environment()
    check_required_keys('OPENAI_API_KEY')
    display_config()

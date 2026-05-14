"""
Script to convert RAG Techniques notebooks with centralized .env configuration
Creates separate folders for each technique with properly configured notebooks
"""

import json
import os
import re
from pathlib import Path
import shutil

# Define the notebook list
NOTEBOOKS = [
    "simple_rag",
    "simple_rag_with_llamaindex",
    "simple_csv_rag",
    "simple_csv_rag_with_llamaindex",
    "Agentic_RAG",
    "HyDe_Hypothetical_Document_Embedding",
    "HyPE_Hypothetical_Prompt_Embeddings",
    "Microsoft_GraphRag",
    "adaptive_retrieval",
    "choose_chunk_size",
    "context_enrichment_window_around_chunk",
    "context_enrichment_window_around_chunk_with_llamaindex",
    "contextual_chunk_headers",
    "contextual_compression",
    "crag",
    "dartboard",
    "document_augmentation",
    "explainable_retrieval",
    "fusion_retrieval",
    "fusion_retrieval_with_llamaindex",
    "graph_rag",
    "graphrag_with_milvus_vectordb",
    "hierarchical_indices",
    "json_rag",
    "memorag",
    "multi_model_rag_with_captioning",
    "multi_model_rag_with_colpali",
    "proposition_chunking",
    "query_transformations",
    "raptor",
    "relevant_segment_extraction",
    "reliable_rag",
    "reranking",
    "reranking_with_llamaindex",
    "retrieval_with_feedback_loop",
    "self_rag",
    "semantic_chunking",
]

def create_env_loading_cell():
    """Create a cell for loading environment variables"""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load environment variables from centralized .env file\n",
            "import sys\n",
            "from pathlib import Path\n",
            "\n",
            "# Add parent directory to path to import utils\n",
            "project_root = Path.cwd().parent\n",
            "if str(project_root) not in sys.path:\n",
            "    sys.path.insert(0, str(project_root))\n",
            "\n",
            "from utils.env_loader import load_environment, check_required_keys, display_config\n",
            "\n",
            "# Load environment variables\n",
            "load_environment()\n",
            "\n",
            "# Check required API keys\n",
            "check_required_keys('OPENAI_API_KEY')\n",
            "\n",
            "# Display current configuration\n",
            "display_config()"
        ]
    }

def create_helper_import_cell():
    """Create a cell for importing helper functions"""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Import helper functions\n",
            "import sys\n",
            "from pathlib import Path\n",
            "\n",
            "# Add utils directory to path\n",
            "utils_dir = Path.cwd().parent / 'utils'\n",
            "if str(utils_dir) not in sys.path:\n",
            "    sys.path.insert(0, str(utils_dir))\n",
            "\n",
            "from helper_functions import *"
        ]
    }

def update_file_paths(cell_source):
    """Update file paths in cell source to point to centralized data directory"""
    if isinstance(cell_source, list):
        cell_source = ''.join(cell_source)

    # Update relative paths to data files
    cell_source = cell_source.replace('../data/', '../../data/')
    cell_source = cell_source.replace('./data/', '../../data/')
    cell_source = cell_source.replace('data/', '../../data/')

    # Update image paths
    cell_source = cell_source.replace('../images/', '../../images/')
    cell_source = cell_source.replace('./images/', '../../images/')

    # Update helper functions import if directly referenced
    cell_source = cell_source.replace('from helper_functions import', 'from utils.helper_functions import')
    cell_source = cell_source.replace('import helper_functions', 'from utils import helper_functions')

    return cell_source

def remove_existing_env_cells(cells):
    """Remove cells that load environment variables or set API keys directly"""
    filtered_cells = []
    skip_next = False

    for i, cell in enumerate(cells):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

            # Skip cells that set API keys directly
            if any(key in source for key in ['os.environ[', 'getpass.getpass', 'OPENAI_API_KEY',
                                              'ANTHROPIC_API_KEY', 'COHERE_API_KEY']):
                if 'from dotenv import load_dotenv' not in source:  # Keep if it's just importing
                    continue

            # Skip cells that import from helper_functions at the top level
            if 'from helper_functions import' in source and i < 10:
                continue

        filtered_cells.append(cell)

    return filtered_cells

def convert_notebook(source_path, dest_folder, notebook_name):
    """Convert a single notebook with proper environment loading"""
    try:
        # Read source notebook
        with open(source_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        # Remove existing environment loading cells
        notebook['cells'] = remove_existing_env_cells(notebook['cells'])

        # Find the first code cell index
        first_code_idx = 0
        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'code':
                first_code_idx = i
                break

        # Insert environment loading cells after first markdown cells
        insert_idx = first_code_idx

        # Add markdown header for setup
        setup_header = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🔧 Environment Setup\n",
                "\n",
                "This notebook uses a centralized `.env` file for configuration. ",
                "Make sure you have set up your API keys in the `.env` file at the project root."
            ]
        }

        notebook['cells'].insert(insert_idx, setup_header)
        notebook['cells'].insert(insert_idx + 1, create_env_loading_cell())
        notebook['cells'].insert(insert_idx + 2, create_helper_import_cell())

        # Update file paths in all cells
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                if isinstance(cell['source'], list):
                    cell['source'] = [update_file_paths(line) for line in cell['source']]
                else:
                    cell['source'] = update_file_paths(cell['source'])

        # Save converted notebook
        dest_path = dest_folder / f"{notebook_name}.ipynb"
        with open(dest_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)

        print(f"✅ Converted: {notebook_name}")
        return True

    except Exception as e:
        print(f"❌ Error converting {notebook_name}: {str(e)}")
        return False

def create_readme(folder_path, technique_name):
    """Create a README for each technique folder"""
    readme_content = f"""# {technique_name.replace('_', ' ').title()}

## Overview

This folder contains the Jupyter notebook implementation for the **{technique_name.replace('_', ' ').title()}** RAG technique.

## Setup

1. Ensure you have configured the `.env` file in the project root with your API keys
2. Install required dependencies: `pip install -r ../../requirements.txt`
3. Open and run the notebook: `{technique_name}.ipynb`

## Configuration

This notebook uses the centralized environment configuration from the project root `.env` file.
Key configurations include:

- OpenAI API Key
- Vector Database credentials
- Model selections
- LangChain settings

## Data

The notebook references data files from the centralized `data/` directory at the project root.

## Running the Notebook

Simply open the notebook in Jupyter Lab or Jupyter Notebook:

```bash
jupyter notebook {technique_name}.ipynb
```

or

```bash
jupyter lab {technique_name}.ipynb
```

The environment will be automatically loaded from the centralized `.env` file.
"""

    readme_path = folder_path / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    """Main conversion function"""
    print("=" * 70)
    print("RAG Techniques Notebook Converter")
    print("=" * 70)
    print()

    # Setup paths
    source_dir = Path("../RAG_Techniques-main/all_rag_techniques")
    base_dir = Path(".")

    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return

    # Create notebooks directory
    notebooks_dir = base_dir / "notebooks"
    notebooks_dir.mkdir(exist_ok=True)

    converted_count = 0
    failed_count = 0

    # Convert each notebook
    for notebook_name in NOTEBOOKS:
        source_file = source_dir / f"{notebook_name}.ipynb"

        if not source_file.exists():
            print(f"⚠️  Notebook not found: {notebook_name}.ipynb")
            failed_count += 1
            continue

        # Create technique folder
        technique_folder = notebooks_dir / notebook_name
        technique_folder.mkdir(exist_ok=True)

        # Convert notebook
        if convert_notebook(source_file, technique_folder, notebook_name):
            converted_count += 1
            # Create README
            create_readme(technique_folder, notebook_name)
        else:
            failed_count += 1

    print()
    print("=" * 70)
    print(f"✅ Successfully converted: {converted_count} notebooks")
    print(f"❌ Failed: {failed_count} notebooks")
    print("=" * 70)
    print()
    print("📁 Notebooks are organized in: ./notebooks/<technique_name>/")
    print("🔧 Don't forget to configure your .env file with API keys!")
    print()
    print("Next steps:")
    print("1. Copy .env.template to .env: cp .env.template .env")
    print("2. Edit .env and add your API keys")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start Jupyter: jupyter lab")

if __name__ == "__main__":
    main()

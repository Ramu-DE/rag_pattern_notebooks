# Hyde Hypothetical Document Embedding

## Overview

This folder contains the Jupyter notebook implementation for the **Hyde Hypothetical Document Embedding** RAG technique.

## Setup

1. Ensure you have configured the `.env` file in the project root with your API keys
2. Install required dependencies: `pip install -r ../../requirements.txt`
3. Open and run the notebook: `HyDe_Hypothetical_Document_Embedding.ipynb`

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
jupyter notebook HyDe_Hypothetical_Document_Embedding.ipynb
```

or

```bash
jupyter lab HyDe_Hypothetical_Document_Embedding.ipynb
```

The environment will be automatically loaded from the centralized `.env` file.

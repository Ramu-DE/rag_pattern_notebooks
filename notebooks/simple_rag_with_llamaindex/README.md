# Simple Rag With Llamaindex

## Overview

This folder contains the Jupyter notebook implementation for the **Simple Rag With Llamaindex** RAG technique.

## Setup

1. Ensure you have configured the `.env` file in the project root with your API keys
2. Install required dependencies: `pip install -r ../../requirements.txt`
3. Open and run the notebook: `simple_rag_with_llamaindex.ipynb`

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
jupyter notebook simple_rag_with_llamaindex.ipynb
```

or

```bash
jupyter lab simple_rag_with_llamaindex.ipynb
```

The environment will be automatically loaded from the centralized `.env` file.

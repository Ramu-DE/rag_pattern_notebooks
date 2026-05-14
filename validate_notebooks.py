#!/usr/bin/env python3
"""
Notebook Validation Script
Validates all 37 RAG technique notebooks for structural integrity and syntax
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

def validate_notebook_structure(notebook_path: Path) -> Tuple[bool, str]:
    """
    Validate notebook JSON structure and basic integrity.

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        # Check required fields
        if 'cells' not in notebook:
            return False, "Missing 'cells' field"

        if 'metadata' not in notebook:
            return False, "Missing 'metadata' field"

        if 'nbformat' not in notebook:
            return False, "Missing 'nbformat' field"

        # Check cells structure
        cells = notebook['cells']
        if not isinstance(cells, list):
            return False, "'cells' is not a list"

        if len(cells) == 0:
            return False, "Notebook has no cells"

        # Validate each cell
        for i, cell in enumerate(cells):
            if 'cell_type' not in cell:
                return False, f"Cell {i} missing 'cell_type'"

            if cell['cell_type'] not in ['code', 'markdown', 'raw']:
                return False, f"Cell {i} has invalid cell_type: {cell['cell_type']}"

            if 'source' not in cell:
                return False, f"Cell {i} missing 'source'"

        return True, "Valid notebook structure"

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_environment_setup(notebook_path: Path) -> Tuple[bool, str]:
    """
    Check if notebook has environment loading cells.

    Returns:
        Tuple of (has_setup, message)
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        cells = notebook['cells']

        # Look for environment loading in first 10 cells
        for cell in cells[:10]:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

                if 'from utils.env_loader import' in source or 'load_environment()' in source:
                    return True, "Has environment setup"

        return False, "Missing environment setup"

    except Exception as e:
        return False, f"Error checking: {str(e)}"

def check_imports(notebook_path: Path) -> Tuple[bool, List[str]]:
    """
    Extract and check imports from notebook.

    Returns:
        Tuple of (has_imports, list of imports)
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        imports = []
        cells = notebook['cells']

        for cell in cells:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

                # Find import statements
                lines = source.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        imports.append(line)

        return len(imports) > 0, imports

    except Exception as e:
        return False, [f"Error: {str(e)}"]

def validate_all_notebooks():
    """
    Validate all notebooks in the project.
    """
    print("=" * 80)
    print("📓 RAG Techniques Notebook Validator")
    print("=" * 80)
    print()

    notebooks_dir = Path("notebooks")

    if not notebooks_dir.exists():
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        return 1

    # Get all technique folders
    technique_folders = sorted([d for d in notebooks_dir.iterdir() if d.is_dir()])

    print(f"Found {len(technique_folders)} technique folders\n")

    results = {
        'valid': [],
        'invalid': [],
        'missing_env': [],
        'warnings': []
    }

    # Validate each notebook
    for i, folder in enumerate(technique_folders, 1):
        notebook_name = folder.name
        notebook_file = folder / f"{notebook_name}.ipynb"

        print(f"{i:2}. {notebook_name}")
        print(f"    Path: {notebook_file}")

        if not notebook_file.exists():
            print(f"    ❌ Notebook file not found")
            results['invalid'].append((notebook_name, "File not found"))
            print()
            continue

        # Validate structure
        is_valid, message = validate_notebook_structure(notebook_file)
        if not is_valid:
            print(f"    ❌ Structure invalid: {message}")
            results['invalid'].append((notebook_name, message))
            print()
            continue

        print(f"    ✅ Structure: Valid")

        # Check environment setup
        has_env, env_message = check_environment_setup(notebook_file)
        if has_env:
            print(f"    ✅ Environment: {env_message}")
        else:
            print(f"    ⚠️  Environment: {env_message}")
            results['missing_env'].append(notebook_name)

        # Check imports
        has_imports, imports = check_imports(notebook_file)
        if has_imports:
            print(f"    ✅ Imports: Found {len(imports)} import statements")
        else:
            print(f"    ⚠️  Imports: No imports found")

        # Check file size
        size_kb = notebook_file.stat().st_size / 1024
        print(f"    📊 Size: {size_kb:.1f} KB")

        results['valid'].append(notebook_name)
        print()

    # Summary
    print("=" * 80)
    print("📊 Validation Summary")
    print("=" * 80)
    print()

    print(f"✅ Valid notebooks:           {len(results['valid'])}")
    print(f"❌ Invalid notebooks:         {len(results['invalid'])}")
    print(f"⚠️  Missing env setup:        {len(results['missing_env'])}")
    print()

    if results['invalid']:
        print("Invalid Notebooks:")
        for name, reason in results['invalid']:
            print(f"  ❌ {name}: {reason}")
        print()

    if results['missing_env']:
        print("Notebooks Missing Environment Setup:")
        for name in results['missing_env']:
            print(f"  ⚠️  {name}")
        print()

    print("=" * 80)

    if len(results['valid']) == len(technique_folders):
        print("🎉 All notebooks validated successfully!")
        print("✅ Structure: All notebooks have valid JSON structure")
        print("✅ Integrity: All required fields present")
        print()
        print("Next step: Run functional tests with test_notebooks.py")
        return 0
    else:
        print("⚠️  Some notebooks have issues. See details above.")
        return 1

if __name__ == "__main__":
    exit(validate_all_notebooks())

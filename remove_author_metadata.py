#!/usr/bin/env python3
"""
Remove author/source metadata from all notebooks
"""

import json
from pathlib import Path

def clean_notebook_metadata(notebook_path):
    """Remove author and source metadata from notebook"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        # Fields to remove from metadata
        fields_to_remove = [
            'author', 'authors', 'creator', 'source',
            'original_author', 'contributor', 'contributors'
        ]

        modified = False

        # Clean top-level metadata
        if 'metadata' in notebook:
            for field in fields_to_remove:
                if field in notebook['metadata']:
                    del notebook['metadata'][field]
                    modified = True

            # Clean kernelspec author info
            if 'kernelspec' in notebook['metadata']:
                if 'author' in notebook['metadata']['kernelspec']:
                    del notebook['metadata']['kernelspec']['author']
                    modified = True

        # Clean cell metadata
        if 'cells' in notebook:
            for cell in notebook['cells']:
                if 'metadata' in cell:
                    for field in fields_to_remove:
                        if field in cell['metadata']:
                            del cell['metadata'][field]
                            modified = True

        # Save if modified
        if modified:
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1)
            return True

        return False

    except Exception as e:
        print(f"Error processing {notebook_path}: {e}")
        return False

def main():
    notebooks_dir = Path("notebooks")

    print("=" * 70)
    print("Removing Author Metadata from All Notebooks")
    print("=" * 70)
    print()

    # Get all notebooks
    notebook_files = list(notebooks_dir.rglob("*.ipynb"))

    print(f"Found {len(notebook_files)} notebooks\n")

    cleaned = 0
    unchanged = 0

    for nb_path in sorted(notebook_files):
        print(f"Processing: {nb_path.parent.name}/{nb_path.name}", end='')

        if clean_notebook_metadata(nb_path):
            print(" ✅ Cleaned")
            cleaned += 1
        else:
            print(" ⏭️  No changes")
            unchanged += 1

    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Total notebooks: {len(notebook_files)}")
    print(f"✅ Cleaned: {cleaned}")
    print(f"⏭️  Unchanged: {unchanged}")
    print()
    print("✅ All author metadata removed!")

if __name__ == "__main__":
    main()

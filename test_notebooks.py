#!/usr/bin/env python3
"""
Notebook Testing Framework
Executes notebooks and captures results (requires dependencies installed)
"""

import json
import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional

def execute_notebook(notebook_path: Path, timeout: int = 600) -> Dict:
    """
    Execute a notebook using nbconvert and capture results.

    Args:
        notebook_path: Path to notebook
        timeout: Timeout in seconds (default 10 minutes)

    Returns:
        Dict with execution results
    """
    result = {
        'notebook': notebook_path.name,
        'path': str(notebook_path),
        'success': False,
        'error': None,
        'execution_time': 0,
        'output_file': None
    }

    try:
        start_time = time.time()

        # Create output directory
        output_dir = notebook_path.parent / "test_output"
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"{notebook_path.stem}_executed.ipynb"

        # Execute notebook using nbconvert
        cmd = [
            'jupyter', 'nbconvert',
            '--to', 'notebook',
            '--execute',
            '--ExecutePreprocessor.timeout=' + str(timeout),
            '--output', str(output_file.absolute()),
            str(notebook_path.absolute())
        ]

        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 10
        )

        execution_time = time.time() - start_time

        if process.returncode == 0:
            result['success'] = True
            result['execution_time'] = execution_time
            result['output_file'] = str(output_file)
        else:
            result['success'] = False
            result['error'] = process.stderr
            result['execution_time'] = execution_time

    except subprocess.TimeoutExpired:
        result['error'] = f"Timeout after {timeout} seconds"
    except Exception as e:
        result['error'] = str(e)

    return result

def test_notebooks_batch(notebooks: list, max_notebooks: Optional[int] = None):
    """
    Test a batch of notebooks.

    Args:
        notebooks: List of notebook paths
        max_notebooks: Maximum number to test (None = all)
    """
    print("=" * 80)
    print("🧪 RAG Techniques Notebook Testing Framework")
    print("=" * 80)
    print()

    # Check if jupyter is installed
    try:
        subprocess.run(['jupyter', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Jupyter not found. Please install:")
        print("   pip install jupyter nbconvert")
        return 1

    print("✅ Jupyter and nbconvert are available")
    print()

    # Limit notebooks if requested
    if max_notebooks:
        notebooks = notebooks[:max_notebooks]
        print(f"Testing first {max_notebooks} notebooks\n")

    results = []
    success_count = 0
    fail_count = 0

    for i, notebook_path in enumerate(notebooks, 1):
        print(f"\n{i}/{len(notebooks)}. Testing: {notebook_path.parent.name}")
        print(f"   File: {notebook_path.name}")
        print(f"   Starting execution...", end='', flush=True)

        result = execute_notebook(notebook_path)
        results.append(result)

        if result['success']:
            print(f" ✅ SUCCESS ({result['execution_time']:.1f}s)")
            success_count += 1
        else:
            print(f" ❌ FAILED")
            print(f"   Error: {result['error'][:200]}")
            fail_count += 1

    # Summary
    print("\n" + "=" * 80)
    print("📊 Testing Summary")
    print("=" * 80)
    print()
    print(f"Total notebooks tested:  {len(notebooks)}")
    print(f"✅ Successful:           {success_count}")
    print(f"❌ Failed:               {fail_count}")
    print(f"Success rate:            {(success_count/len(notebooks)*100):.1f}%")
    print()

    if fail_count > 0:
        print("Failed Notebooks:")
        for result in results:
            if not result['success']:
                print(f"  ❌ {result['notebook']}")
                if result['error']:
                    error_preview = result['error'][:150].replace('\n', ' ')
                    print(f"     {error_preview}...")
        print()

    # Save detailed results
    results_file = Path("test_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"📄 Detailed results saved to: {results_file}")

    print("=" * 80)

    return 0 if fail_count == 0 else 1

def main():
    """Main testing function"""
    import argparse

    parser = argparse.ArgumentParser(description='Test RAG Techniques notebooks')
    parser.add_argument('--quick', action='store_true',
                       help='Quick test - only test first 3 notebooks')
    parser.add_argument('--notebook', type=str,
                       help='Test specific notebook by name')
    parser.add_argument('--max', type=int,
                       help='Maximum number of notebooks to test')

    args = parser.parse_args()

    notebooks_dir = Path("notebooks")

    if not notebooks_dir.exists():
        print(f"❌ Notebooks directory not found: {notebooks_dir}")
        return 1

    # Get all notebooks
    all_notebooks = []
    for folder in sorted(notebooks_dir.iterdir()):
        if folder.is_dir():
            notebook_file = folder / f"{folder.name}.ipynb"
            if notebook_file.exists():
                all_notebooks.append(notebook_file)

    if not all_notebooks:
        print("❌ No notebooks found")
        return 1

    # Filter based on arguments
    if args.notebook:
        all_notebooks = [nb for nb in all_notebooks if args.notebook in nb.name]
        if not all_notebooks:
            print(f"❌ Notebook not found: {args.notebook}")
            return 1

    max_count = args.max
    if args.quick:
        max_count = 3

    return test_notebooks_batch(all_notebooks, max_count)

if __name__ == "__main__":
    exit(main())

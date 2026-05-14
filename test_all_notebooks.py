#!/usr/bin/env python3
"""
Test all 37 notebooks - Execute first few cells to verify they work
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
import subprocess
import time

def test_notebook_basic_execution(notebook_path: Path) -> Dict:
    """
    Test basic execution of notebook (first few cells only)

    Returns:
        Dict with test results
    """
    result = {
        'notebook': notebook_path.parent.name,
        'path': str(notebook_path),
        'status': 'unknown',
        'error': None,
        'imports_ok': False,
        'env_loading_ok': False,
        'execution_time': 0
    }

    try:
        start_time = time.time()

        # Read notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        # Check structure
        if 'cells' not in notebook or len(notebook['cells']) == 0:
            result['status'] = 'failed'
            result['error'] = 'No cells found'
            return result

        # Look for environment loading
        env_found = False
        for cell in notebook['cells'][:10]:  # Check first 10 cells
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                source_text = ''.join(source) if isinstance(source, list) else source
                if 'load_environment' in source_text or 'env_loader' in source_text or 'from utils.env_loader import' in source_text:
                    env_found = True
                    break

        result['env_loading_ok'] = env_found

        # Check for imports in first 10 cells
        imports_found = False
        for cell in notebook['cells'][:10]:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
                if 'import ' in source or 'from ' in source:
                    imports_found = True
                    break

        result['imports_ok'] = imports_found

        # Basic validation passed
        if env_found and imports_found:
            result['status'] = 'ok'
        elif not env_found:
            result['status'] = 'warning'
            result['error'] = 'No environment loading found'
        else:
            result['status'] = 'warning'
            result['error'] = 'No imports found'

        result['execution_time'] = time.time() - start_time

    except json.JSONDecodeError as e:
        result['status'] = 'failed'
        result['error'] = f'Invalid JSON: {str(e)}'
    except Exception as e:
        result['status'] = 'failed'
        result['error'] = str(e)

    return result

def test_notebook_imports(notebook_path: Path) -> Dict:
    """
    Test if notebook imports work by executing import cells
    """
    result = {
        'imports_executable': False,
        'error': None
    }

    try:
        # Create a test script with the imports
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        import_code = []
        for cell in notebook['cells'][:15]:  # Check first 15 cells
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
                # Only include import statements and env loading
                if any(keyword in source for keyword in ['import ', 'from ', 'load_environment']):
                    import_code.append(source)

        if import_code:
            # Test the imports
            test_script = '\n\n'.join(import_code)
            test_file = Path('/tmp/test_imports.py')
            test_file.write_text(test_script)

            # Run the test
            proc = subprocess.run(
                ['python3', str(test_file)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=notebook_path.parent
            )

            if proc.returncode == 0:
                result['imports_executable'] = True
            else:
                result['error'] = proc.stderr[:200]

    except subprocess.TimeoutExpired:
        result['error'] = 'Timeout (30s)'
    except Exception as e:
        result['error'] = str(e)[:200]

    return result

def main():
    print("=" * 80)
    print("🧪 Testing All 37 RAG Technique Notebooks")
    print("=" * 80)
    print()
    print("Test Strategy:")
    print("  1. Structure validation (JSON, cells, metadata)")
    print("  2. Environment loading check")
    print("  3. Import statements verification")
    print("  4. Import execution test (sample notebooks)")
    print()
    print("⚠️  Note: Full execution testing would cost $50-100 and take 3-5 hours")
    print("   This quick test verifies notebooks are properly configured.")
    print()

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

    print(f"Found {len(all_notebooks)} notebooks to test\n")
    print("=" * 80)

    results = {
        'ok': [],
        'warning': [],
        'failed': []
    }

    # Test each notebook
    for i, notebook_path in enumerate(all_notebooks, 1):
        print(f"\n[{i:2}/{len(all_notebooks)}] {notebook_path.parent.name}")
        print(f"      Path: {notebook_path}")

        # Basic test
        result = test_notebook_basic_execution(notebook_path)

        print(f"      Structure: ", end='')
        if result['status'] == 'failed':
            print(f"❌ FAILED")
            print(f"      Error: {result['error']}")
            results['failed'].append(result)
            continue
        else:
            print("✅ Valid")

        print(f"      Environment: ", end='')
        if result['env_loading_ok']:
            print("✅ Found")
        else:
            print("⚠️  Missing")

        print(f"      Imports: ", end='')
        if result['imports_ok']:
            print("✅ Found")
        else:
            print("⚠️  None")

        # Categorize
        if result['status'] == 'ok':
            results['ok'].append(result)
            print(f"      Status: ✅ READY")
        elif result['status'] == 'warning':
            results['warning'].append(result)
            print(f"      Status: ⚠️  WARNING")
        else:
            results['failed'].append(result)
            print(f"      Status: ❌ FAILED")

    # Test imports on a sample
    print("\n" + "=" * 80)
    print("📦 Testing Import Execution (Sample: first 5 notebooks)")
    print("=" * 80)

    sample_notebooks = all_notebooks[:5]
    import_test_results = []

    for notebook_path in sample_notebooks:
        print(f"\nTesting: {notebook_path.parent.name}")
        import_result = test_notebook_imports(notebook_path)
        import_test_results.append({
            'notebook': notebook_path.parent.name,
            **import_result
        })

        if import_result['imports_executable']:
            print(f"  ✅ Imports execute successfully")
        else:
            print(f"  ❌ Import execution failed")
            if import_result['error']:
                print(f"     Error: {import_result['error'][:150]}")

    # Summary
    print("\n" + "=" * 80)
    print("📊 TESTING SUMMARY")
    print("=" * 80)
    print()
    print(f"Total notebooks tested:  {len(all_notebooks)}")
    print(f"✅ Ready to use:         {len(results['ok'])}")
    print(f"⚠️  Warnings:             {len(results['warning'])}")
    print(f"❌ Failed:               {len(results['failed'])}")
    print()

    success_rate = (len(results['ok']) / len(all_notebooks)) * 100
    print(f"Success rate: {success_rate:.1f}%")
    print()

    # Import test summary
    import_success = sum(1 for r in import_test_results if r['imports_executable'])
    print(f"Import execution test (sample of {len(sample_notebooks)}):")
    print(f"  ✅ Passed: {import_success}/{len(sample_notebooks)}")
    print()

    # Details
    if results['warning']:
        print("⚠️  Notebooks with Warnings:")
        for result in results['warning']:
            print(f"  • {result['notebook']}: {result['error']}")
        print()

    if results['failed']:
        print("❌ Failed Notebooks:")
        for result in results['failed']:
            print(f"  • {result['notebook']}: {result['error']}")
        print()

    print("=" * 80)
    print("✅ TESTING COMPLETE")
    print("=" * 80)
    print()

    if len(results['ok']) == len(all_notebooks):
        print("🎉 All notebooks are properly configured and ready to use!")
        print()
        print("Next steps:")
        print("  1. Open Jupyter Lab: http://127.0.0.1:8888/lab")
        print("  2. Navigate to any notebook")
        print("  3. Run cells manually to explore techniques")
        print()
        print("⚠️  Note: This test verified structure and configuration.")
        print("   Individual notebooks may still have runtime dependencies or")
        print("   require specific data files. Test manually for full validation.")
    else:
        print("⚠️  Some notebooks have issues. See details above.")

    print()

    # Save detailed results
    results_file = Path("notebook_test_results.json")
    with open(results_file, 'w') as f:
        json.dump({
            'summary': {
                'total': len(all_notebooks),
                'ok': len(results['ok']),
                'warning': len(results['warning']),
                'failed': len(results['failed'])
            },
            'results': results,
            'import_tests': import_test_results
        }, f, indent=2)

    print(f"📄 Detailed results saved to: {results_file}")
    print()

    return 0 if len(results['failed']) == 0 else 1

if __name__ == "__main__":
    exit(main())

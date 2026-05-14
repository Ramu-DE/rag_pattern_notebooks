"""
Verification script to check the RAG Techniques Notebooks setup
Run this to ensure everything is properly configured
"""

import sys
from pathlib import Path
import json

def check_file_exists(path, description):
    """Check if a file exists and report status"""
    if path.exists():
        print(f"  ✅ {description}: {path}")
        return True
    else:
        print(f"  ❌ {description} NOT FOUND: {path}")
        return False

def check_notebooks():
    """Verify all notebooks are present and valid"""
    notebooks_dir = Path("notebooks")

    if not notebooks_dir.exists():
        print("❌ Notebooks directory not found!")
        return False

    technique_folders = sorted([d for d in notebooks_dir.iterdir() if d.is_dir()])

    print(f"\n📚 Checking {len(technique_folders)} technique folders...\n")

    all_valid = True
    for folder in technique_folders:
        notebook_file = folder / f"{folder.name}.ipynb"
        readme_file = folder / "README.md"

        has_notebook = notebook_file.exists()
        has_readme = readme_file.exists()

        if has_notebook and has_readme:
            # Verify notebook is valid JSON
            try:
                with open(notebook_file, 'r') as f:
                    json.load(f)
                status = "✅"
            except json.JSONDecodeError:
                status = "⚠️  (Invalid JSON)"
                all_valid = False
        elif has_notebook:
            status = "⚠️  (Missing README)"
        else:
            status = "❌"
            all_valid = False

        print(f"  {status} {folder.name}")

    return all_valid

def check_environment():
    """Check environment configuration"""
    print("\n🔧 Checking environment files...\n")

    env_file = Path(".env")
    env_template = Path(".env.template")

    has_template = check_file_exists(env_template, ".env.template")
    has_env = check_file_exists(env_file, ".env")

    if not has_env:
        print("\n  ⚠️  WARNING: .env file not found!")
        print("  Please create it from template: cp .env.template .env")
        print("  Then add your API keys to .env")
        return False

    # Check if .env has actual keys (not just template)
    with open(env_file, 'r') as f:
        content = f.read()

    if 'OPENAI_API_KEY=' in content and '=' in content:
        lines = [l for l in content.split('\n') if 'API_KEY=' in l and not l.strip().startswith('#')]
        empty_keys = [l for l in lines if l.split('=')[1].strip() == '']

        if empty_keys:
            print(f"\n  ⚠️  Found {len(empty_keys)} empty API key(s) in .env")
            print("  Please add your actual API keys to .env file")
            return False
        else:
            print("\n  ✅ .env file appears to be configured")
            return True

    return True

def check_utils():
    """Check utility files"""
    print("\n🛠️  Checking utility files...\n")

    utils_dir = Path("utils")

    files = [
        (utils_dir / "__init__.py", "utils/__init__.py"),
        (utils_dir / "env_loader.py", "utils/env_loader.py"),
        (utils_dir / "helper_functions.py", "utils/helper_functions.py"),
    ]

    all_present = True
    for file_path, description in files:
        if not check_file_exists(file_path, description):
            all_present = False

    return all_present

def check_data_and_images():
    """Check data and images directories"""
    print("\n📁 Checking data and images...\n")

    data_dir = Path("data")
    images_dir = Path("images")

    has_data = check_file_exists(data_dir, "data/")
    has_images = check_file_exists(images_dir, "images/")

    if has_data:
        data_files = list(data_dir.glob("*"))
        print(f"     Found {len(data_files)} files in data/")

    if has_images:
        image_files = list(images_dir.glob("*"))
        print(f"     Found {len(image_files)} files in images/")

    return has_data and has_images

def check_requirements():
    """Check requirements.txt"""
    print("\n📦 Checking dependencies...\n")

    req_file = Path("requirements.txt")
    has_req = check_file_exists(req_file, "requirements.txt")

    if has_req:
        with open(req_file, 'r') as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
        print(f"     Found {len(lines)} package dependencies")

    return has_req

def check_documentation():
    """Check documentation files"""
    print("\n📖 Checking documentation...\n")

    files = [
        (Path("README.md"), "README.md"),
        (Path("QUICKSTART.md"), "QUICKSTART.md"),
        (Path("INDEX.ipynb"), "INDEX.ipynb (Master Index)"),
    ]

    all_present = True
    for file_path, description in files:
        if not check_file_exists(file_path, description):
            all_present = False

    return all_present

def main():
    """Run all verification checks"""
    print("=" * 70)
    print("RAG Techniques Notebooks - Setup Verification")
    print("=" * 70)

    checks = [
        ("Environment Configuration", check_environment),
        ("Utility Files", check_utils),
        ("Notebooks", check_notebooks),
        ("Data & Images", check_data_and_images),
        ("Requirements", check_requirements),
        ("Documentation", check_documentation),
    ]

    results = {}

    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Error checking {name}: {str(e)}")
            results[name] = False

    # Summary
    print("\n" + "=" * 70)
    print("Verification Summary")
    print("=" * 70 + "\n")

    for name, status in results.items():
        icon = "✅" if status else "❌"
        print(f"  {icon} {name}")

    all_passed = all(results.values())

    print("\n" + "=" * 70)

    if all_passed:
        print("✅ All checks passed! Your setup is ready to go!")
        print("\nNext steps:")
        print("1. Make sure your .env file has your API keys")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Start Jupyter: jupyter lab")
        print("4. Open INDEX.ipynb for navigation")
    else:
        print("⚠️  Some checks failed. Please review the output above.")
        print("\nTo fix:")
        print("1. Ensure you ran convert_notebooks.py")
        print("2. Copy .env.template to .env and add your keys")
        print("3. Check that all files were properly created")

    print("=" * 70)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

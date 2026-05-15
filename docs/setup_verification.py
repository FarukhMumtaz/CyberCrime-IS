"""
Cyber Crime Reporting System - Setup and Diagnostics Script

This script validates the project structure and identifies any issues.
Run this after installation to ensure all components are properly configured.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def print_header(title: str):
    """Print formatted header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def check_python_version():
    """Check Python version."""
    print_header("Python Version Check")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required")
        return False
    print("✓ Python version is compatible")
    return True

def check_project_structure():
    """Verify project structure."""
    print_header("Project Structure Verification")
    
    required_dirs = [
        'frontend',
        'backend',
        'backend/api',
        'backend/services',
        'backend/models',
        'backend/utils',
        'backend/tests',
        'database',
        'database/schemas',
        'database/migrations',
        'docs',
        'deployment'
    ]
    
    all_exist = True
    for directory in required_dirs:
        path = Path(directory)
        if path.exists():
            print(f"✓ {directory}")
        else:
            print(f"❌ {directory} - MISSING")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if required packages are installed."""
    print_header("Dependencies Check")
    
    required_packages = [
        'streamlit',
        'fastapi',
        'uvicorn',
        'supabase',
        'pydantic',
        'cryptography',
        'groq',
        'jwt',
        'python-dotenv',
        'reportlab',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    return len(missing) == 0, missing

def check_env_file():
    """Check if .env file exists."""
    print_header("Environment Configuration")
    
    if Path('.env').exists():
        print("✓ .env file exists")
        
        # Check for essential variables
        required_vars = [
            'JWT_SECRET_KEY',
            'ENCRYPTION_KEY',
            'SUPABASE_URL',
            'SUPABASE_ANON_KEY',
            'GROQ_API_KEY'
        ]
        
        with open('.env', 'r') as f:
            env_content = f.read()
        
        missing_vars = []
        for var in required_vars:
            if var in env_content:
                print(f"✓ {var} - configured")
            else:
                print(f"⚠ {var} - NOT CONFIGURED")
                missing_vars.append(var)
        
        return len(missing_vars) == 0
    else:
        print("⚠ .env file not found")
        print("  Run: cp .env.example .env")
        return False

def check_imports():
    """Test Python imports."""
    print_header("Python Imports Verification")
    
    test_imports = {
        'Frontend': [
            ('streamlit', 'Streamlit'),
            ('pages', 'Frontend pages module')
        ],
        'Backend': [
            ('api.main', 'FastAPI main'),
            ('services', 'Services layer'),
            ('models', 'Data models'),
            ('utils.security', 'Security utilities')
        ]
    }
    
    all_ok = True
    for category, imports_list in test_imports.items():
        print(f"\n{category}:")
        for module, description in imports_list:
            try:
                if category == 'Backend':
                    sys.path.insert(0, 'backend')
                    __import__(module)
                    sys.path.pop(0)
                else:
                    __import__(module)
                print(f"  ✓ {description}")
            except ImportError as e:
                print(f"  ❌ {description}: {e}")
                all_ok = False
    
    return all_ok

def check_database_setup():
    """Check database schema files."""
    print_header("Database Setup Verification")
    
    schema_files = [
        'database/schemas/main_schema.sql',
        'database/migrations/001_initial_setup.sql',
        'database/seeders/cyber_laws.sql'
    ]
    
    all_exist = True
    for file in schema_files:
        path = Path(file)
        if path.exists():
            size = path.stat().st_size
            print(f"✓ {file} ({size} bytes)")
        else:
            print(f"❌ {file} - MISSING")
            all_exist = False
    
    return all_exist

def check_documentation():
    """Check documentation files."""
    print_header("Documentation Verification")
    
    doc_files = [
        'docs/api/api_documentation.md',
        'docs/architecture/system_architecture.md',
        'docs/guides/user_guide.md',
        'deployment/streamlit_cloud_guide.md'
    ]
    
    found = 0
    for file in doc_files:
        path = Path(file)
        if path.exists():
            lines = sum(1 for _ in open(path))
            print(f"✓ {file} ({lines} lines)")
            found += 1
        else:
            print(f"⚠ {file} - MISSING")
    
    return found == len(doc_files)

def generate_report(results: dict):
    """Generate final report."""
    print_header("Setup Verification Report")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Report Generated: {timestamp}\n")
    
    status_map = {
        True: "✓ PASS",
        False: "❌ FAIL",
        None: "⚠ PARTIAL"
    }
    
    print("Verification Results:")
    print("-" * 80)
    
    for check_name, result in results.items():
        status = status_map.get(result, "? UNKNOWN")
        print(f"{check_name:.<50} {status}")
    
    print("-" * 80)
    
    all_passed = all(v for v in results.values() if v is not None)
    
    if all_passed:
        print("\n✓ All checks passed! System is ready for development.")
    else:
        print("\n⚠ Some checks failed. Review the output above for details.")
        print("\nNext Steps:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Configure environment: cp .env.example .env")
        print("3. Set up Supabase with database schemas from database/ folder")
        print("4. Verify all API keys are valid")
    
    return all_passed

def main():
    """Run all checks."""
    print(f"\n{'='*80}")
    print("  Cyber Crime Reporting System - Setup Verification")
    print(f"{'='*80}")
    
    results = {}
    
    # Run checks
    results['Python Version'] = check_python_version()
    results['Project Structure'] = check_project_structure()
    results['Environment Variables'] = check_env_file()
    
    # Check dependencies
    deps_ok, missing_deps = check_dependencies()
    results['Dependencies'] = deps_ok
    if missing_deps:
        print(f"\nMissing packages: {', '.join(missing_deps)}")
        print("Install with: pip install -r requirements.txt\n")
    
    # Check imports (only if dependencies mostly ok)
    if deps_ok:
        results['Python Imports'] = check_imports()
    
    results['Database Files'] = check_database_setup()
    results['Documentation'] = check_documentation()
    
    # Generate report
    all_passed = generate_report(results)
    
    # Print quick start guide if all passed
    if all_passed:
        print("\n" + "="*80)
        print("  Quick Start Guide")
        print("="*80)
        print("\n1. Start the Frontend (Streamlit):")
        print("   streamlit run frontend/app.py")
        print("\n2. Start the Backend API (in a new terminal):")
        print("   cd backend/api && python main.py")
        print("\n3. Access the application:")
        print("   Frontend: http://localhost:8501")
        print("   Backend API: http://localhost:8000/docs")
        print("\n" + "="*80 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

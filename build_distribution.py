#!/usr/bin/env python3
"""
Build distribution packages for Job Application Auto-Fill Bot
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}")

def build_package():
    """Build the Python package."""
    print("Building Python package...")
    try:
        subprocess.run([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'], check=True)
        print("Package built successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error building package: {e}")
        return False
    return True

def create_zip_package():
    """Create a simple zip package for non-technical users."""
    print("Creating zip package...")
    
    # Files to include in zip
    files_to_include = [
        'main.py',
        'form_filler.py',
        'config.py',
        'config_manager.py',
        'gui_config.py',
        'quick_start.py',
        'application_tracker.py',
        'auto_updater.py',
        'requirements.txt',
        'environment.yml',
        'README.md',
        'setup_conda.md',
        'LICENSE'
    ]
    
    # Create distribution directory
    dist_dir = Path('dist_zip')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copy files
    for file_name in files_to_include:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_dir)
            print(f"Copied {file_name}")
    
    # Create zip
    zip_name = 'job-application-autofill-bot.zip'
    shutil.make_archive('job-application-autofill-bot', 'zip', dist_dir)
    
    # Clean up
    shutil.rmtree(dist_dir)
    print(f"Created {zip_name}")

def create_installer_script():
    """Create an installer script for easy setup."""
    installer_content = '''#!/usr/bin/env python3
"""
Quick installer for Job Application Auto-Fill Bot
"""

import os
import sys
import subprocess
import platform

def main():
    print("Job Application Auto-Fill Bot - Quick Installer")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        return
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    
    # Install dependencies
    print("\\nInstalling dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return
    
    # Create sample config if it doesn't exist
    if not os.path.exists('config.py'):
        print("\\nCreating sample configuration...")
        try:
            subprocess.run([sys.executable, 'quick_start.py'], check=True)
            print("Sample configuration created!")
        except subprocess.CalledProcessError as e:
            print(f"Error creating configuration: {e}")
    
    print("\\nInstallation complete!")
    print("\\nTo start the application:")
    print("  python main.py")
    print("\\nTo configure your information:")
    print("  python config_manager.py")
    print("\\nFor help:")
    print("  python main.py --help")

if __name__ == "__main__":
    main()
'''
    
    with open('install.py', 'w') as f:
        f.write(installer_content)
    
    print("Created install.py")

def main():
    """Main build process."""
    print("Building Job Application Auto-Fill Bot distribution...")
    print("=" * 60)
    
    # Clean previous builds
    clean_build()
    
    # Build Python package
    if build_package():
        print("\\nPython package distribution created in 'dist/' directory")
    
    # Create zip package
    create_zip_package()
    
    # Create installer script
    create_installer_script()
    
    print("\\n" + "=" * 60)
    print("Distribution build complete!")
    print("\\nCreated:")
    print("- Python package (dist/)")
    print("- Zip package (job-application-autofill-bot.zip)")
    print("- Installer script (install.py)")
    print("\\nNext steps:")
    print("1. Upload to GitHub")
    print("2. Create releases with the zip file")
    print("3. Share the install.py script for easy setup")

if __name__ == "__main__":
    main() 
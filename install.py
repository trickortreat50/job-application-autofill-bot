#!/usr/bin/env python3
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
    print("\nInstalling dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return
    
    # Create sample config if it doesn't exist
    if not os.path.exists('config.py'):
        print("\nCreating sample configuration...")
        try:
            subprocess.run([sys.executable, 'quick_start.py'], check=True)
            print("Sample configuration created!")
        except subprocess.CalledProcessError as e:
            print(f"Error creating configuration: {e}")
    
    print("\nInstallation complete!")
    print("\nTo start the application:")
    print("  python main.py")
    print("\nTo configure your information:")
    print("  python config_manager.py")
    print("\nFor help:")
    print("  python main.py --help")

if __name__ == "__main__":
    main()

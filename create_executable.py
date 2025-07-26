#!/usr/bin/env python3
"""
Create standalone executable for Job Application Auto-Fill Bot
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller installed successfully!")

def create_executable():
    """Create the standalone executable."""
    print("Creating standalone executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (for GUI)
        "--name=JobAutoFillBot",  # Name of the executable
        "--icon=icon.ico",  # Icon file (if exists)
        "--add-data=config.py;.",  # Include config file
        "--add-data=requirements.txt;.",  # Include requirements
        "--add-data=README.md;.",  # Include README
        "main.py"
    ]
    
    # Remove icon option if icon doesn't exist
    if not os.path.exists("icon.ico"):
        cmd = [arg for arg in cmd if not arg.startswith("--icon")]
    
    try:
        subprocess.run(cmd, check=True)
        print("Executable created successfully!")
        print("Location: dist/JobAutoFillBot.exe")
        
        # Create a simple launcher script
        create_launcher_script()
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating executable: {e}")
        return False
    
    return True

def create_launcher_script():
    """Create a simple launcher script for the executable."""
    launcher_content = '''@echo off
echo Job Application Auto-Fill Bot
echo =============================
echo.
echo Starting the application...
echo.
JobAutoFillBot.exe
pause
'''
    
    with open("launch.bat", "w") as f:
        f.write(launcher_content)
    
    print("Created launch.bat for easy execution")

def create_installer_script():
    """Create an installer script for the executable version."""
    installer_content = '''@echo off
echo Job Application Auto-Fill Bot - Executable Installer
echo ===================================================
echo.
echo This will install the Job Application Auto-Fill Bot on your system.
echo.
echo Requirements:
echo - Windows 10 or later
echo - No Python installation required
echo.
pause

echo.
echo Installing...
echo.

REM Create program directory
if not exist "%PROGRAMFILES%\\JobAutoFillBot" mkdir "%PROGRAMFILES%\\JobAutoFillBot"

REM Copy files
copy "JobAutoFillBot.exe" "%PROGRAMFILES%\\JobAutoFillBot\\"
copy "launch.bat" "%PROGRAMFILES%\\JobAutoFillBot\\"
copy "README.md" "%PROGRAMFILES%\\JobAutoFillBot\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Job Auto-Fill Bot.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\JobAutoFillBot\\launch.bat'; $Shortcut.Save()"

echo.
echo Installation complete!
echo.
echo You can now run the application from:
echo - Desktop shortcut
echo - Start menu
echo - %PROGRAMFILES%\\JobAutoFillBot\\launch.bat
echo.
pause
'''
    
    with open("install_executable.bat", "w") as f:
        f.write(installer_content)
    
    print("Created install_executable.bat")

def main():
    """Main function."""
    print("Creating standalone executable for Job Application Auto-Fill Bot")
    print("=" * 70)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create executable
    if create_executable():
        # Create installer
        create_installer_script()
        
        print("\n" + "=" * 70)
        print("Executable creation complete!")
        print("\nCreated:")
        print("- JobAutoFillBot.exe (in dist/ folder)")
        print("- launch.bat (for easy execution)")
        print("- install_executable.bat (for system installation)")
        print("\nTo distribute:")
        print("1. Share the dist/JobAutoFillBot.exe file")
        print("2. Or share the entire dist/ folder")
        print("3. Or create an installer package")
    else:
        print("Failed to create executable.")

if __name__ == "__main__":
    main() 